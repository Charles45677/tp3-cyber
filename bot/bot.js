const puppeteer = require('puppeteer');

(async () => {
    
    const browser = await puppeteer.launch({ 
        headless: false,
    });
    const page = await browser.newPage();
    
  
    await page.goto('http://localhost:15556/');

    while (true) {
        
        const randomId = Math.random().toString(36).substring(2, 8);
        
       
        await page.waitForSelector('#champ-texte');
        await page.type('#champ-texte', `je suis ${randomId}`);
        
        
        await page.waitForSelector('#bouton-envoyer');
        await page.click('#bouton-envoyer');


        
        await new Promise(r => setTimeout(r, 5000));
    }
})();
