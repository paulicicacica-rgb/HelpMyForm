export default async function handler(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { imageBase64, imageMime, language } = req.body;

  if (!imageBase64 || !imageMime) {
    return res.status(400).json({ error: 'Missing image data' });
  }

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: 'Server configuration error' });
  }

  const langName = language || 'English';

  const prompt = `You are FormGuide, a helpful assistant that helps people fill in official forms.

The user has photographed a form. Please:

1. IDENTIFY the form — what is it called, what organisation/government issued it, what is it for? (2-3 sentences max)

2. LIST what documents/information the user needs to have ready BEFORE filling it

3. GO THROUGH EACH FIELD one by one — for every field/section on the form:
   - Field name/number
   - What it's asking for in plain simple language
   - An example of what to write (where helpful)
   - Any important warnings or notes

4. CREATE A CHECKLIST of everything the user needs to submit or prepare

Please respond in ${langName}. Use simple, clear language. Avoid jargon. Format your response EXACTLY like this:

FORM_NAME: [name of the form]
FORM_ORG: [issuing organisation]
FORM_PURPOSE: [what it's for in 1-2 sentences]

BEFORE_YOU_START:
- [item 1]
- [item 2]
...

FIELDS:
FIELD: [field name or number]
EXPLAIN: [plain language explanation]
EXAMPLE: [example of what to write, or "N/A"]
---
FIELD: [next field]
EXPLAIN: [explanation]
EXAMPLE: [example]
---
...

CHECKLIST:
- [checklist item 1]
- [checklist item 2]
...`;

  const callGemini = async () => {
    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{
            parts: [
              { text: prompt },
              { inline_data: { mime_type: imageMime, data: imageBase64 } }
            ]
          }],
          generationConfig: { temperature: 0.3, maxOutputTokens: 4096 }
        })
      }
    );
    return response;
  };

  const sleep = (ms) => new Promise(r => setTimeout(r, ms));

  const MAX_RETRIES = 3;
  const RETRY_DELAY = 3000;

  try {
    let response;
    let lastError;

    for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
      response = await callGemini();

      if (response.ok) break;

      const err = await response.json();
      lastError = err.error?.message || 'Gemini API error';
      const status = response.status;

      // Only retry on busy/overload errors (429, 503)
      if (status === 429 || status === 503) {
        if (attempt < MAX_RETRIES) {
          await sleep(RETRY_DELAY);
          continue;
        }
      }

      // For other errors don't retry
      return res.status(502).json({ error: lastError });
    }

    if (!response.ok) {
      return res.status(502).json({ error: lastError || 'Gemini API error' });
    }

    const data = await response.json();
    const text = data.candidates?.[0]?.content?.parts?.[0]?.text;
    if (!text) return res.status(502).json({ error: 'No response from AI' });

    return res.status(200).json({ result: text });

  } catch (err) {
    console.error('analyze error:', err);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
