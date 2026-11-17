const puppeteer = require('puppeteer');

(async () => {
    //  Ouvre le navigateur
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();
    
    
    await page.goto('`a ch=anger.https');

    let id = 1;

    
    while (true) {
       
        await page.type('#champ-texte', `${id} - Mon message auto`);
        
        
        await page.click('#bouton-envoyer');

        console.log(`Message #${id} envoyé.`);
        id++;

       
        await new Promise(r => setTimeout(r, 5000));
    }
})();
