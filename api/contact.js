export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { name, email, message } = req.body;
  if (!name || !email || !message) return res.status(400).json({ error: 'Missing fields' });

  try {
    const response = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer re_izv3LfHj_P71gSuT27Rj9UVhaNDEBoBg4`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        from: 'HelpMyForm <onboarding@resend.dev>',
        to: ['support@helpmyform.com'],
        reply_to: email,
        subject: `HelpMyForm contact: ${name}`,
        text: `Name: ${name}\nEmail: ${email}\n\nMessage:\n${message}`
      })
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.message || 'Resend error');
    }

    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Contact error:', err);
    return res.status(500).json({ error: 'Failed to send' });
  }
}
