export default async function handler(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { message, formContext, chatHistory, language } = req.body;

  if (!message || !formContext) {
    return res.status(400).json({ error: 'Missing message or form context' });
  }

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: 'Server configuration error' });
  }

  const langName = language || 'English';
  const historyText = (chatHistory || [])
    .slice(0, -1)
    .map(m => `${m.role}: ${m.text}`)
    .join('\n');

  const systemPrompt = `You are FormGuide, a helpful assistant. The user has scanned a form and received this analysis:

${formContext}

Now help the user with any follow-up questions about this form. Be brief, clear, and helpful. Respond in ${langName}. Previous conversation: ${historyText}`;

  try {
    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{
            parts: [{ text: systemPrompt + '\n\nUser question: ' + message }]
          }],
          generationConfig: { temperature: 0.4, maxOutputTokens: 512 }
        })
      }
    );

    if (!response.ok) {
      const err = await response.json();
      return res.status(502).json({ error: err.error?.message || 'Gemini API error' });
    }

    const data = await response.json();
    const reply = data.candidates?.[0]?.content?.parts?.[0]?.text;
    if (!reply) return res.status(502).json({ error: 'No response from AI' });

    return res.status(200).json({ reply });

  } catch (err) {
    console.error('chat error:', err);
    return res.status(500).json({ error: 'Internal server error' });
  }
}

