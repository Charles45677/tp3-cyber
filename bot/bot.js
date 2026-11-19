const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({
    executablePath: process.env.PUPPETEER_EXECUTABLE_PATH || '/usr/bin/chromium',
    headless: true,
    args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--no-zygote',
        '--disable-gpu'
    ]
});

    const page = await browser.newPage();
    
  
  await page.goto('http://ctf_frontend:15556/faq');

<<<<<<< HEAD

    const page = await browser.newPage();

=======
>>>>>>> 3a17abc (fix du bot)
    const targetUrl = process.env.TARGET_URL || 'http://ctf_frontend:15556/faq';

    while (true) {
        const randomId = Math.random().toString(36).substring(2, 8);
        const messageToSend = `je suis ${randomId}`;

        try {
            await page.goto(targetUrl, { waitUntil: 'domcontentloaded', timeout: 10000 });

            const inputSelector = '[name="message"]';
            await page.waitForSelector(inputSelector, { timeout: 5000 });

            await page.type(inputSelector, messageToSend);

            const submitSelector = 'button[type="submit"], input[type="submit"], button';
            await Promise.all([
                page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 10000 }),
                page.click(submitSelector)
            ]);

            const pageContent = await page.content();
            if (pageContent.includes('Message ajouté à la FAQ.')) {
                console.log(`[OK] Message envoyé : ${messageToSend}`);
            } else {
                console.warn(`[ATTENTION] Formulaire soumis mais pas de confirmation pour : ${messageToSend}`);
            }
        } catch (error) {
            console.error('[ERREUR BOT] :', error.message);
        }

        await new Promise((r) => setTimeout(r, 5000));
    }
})();
