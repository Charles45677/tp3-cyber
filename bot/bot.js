const puppeteer = require('puppeteer');

(async () => {
    
    const browser = await puppeteer.launch({ 
        headless: false,
    });
    const page = await browser.newPage();
    
  
    await page.goto('http://localhost:15556/');

   
        
    while (true) {
        
        const randomId = Math.random().toString(36).substring(2, 8);
        const messageToSend = `je suis ${randomId}`;
        
        try {
           
            const inputSelector = 'input[name="message"], textarea[name="message"]';
            await page.waitForSelector(inputSelector);
            
           
            await page.click(inputSelector, { clickCount: 3 }); 
            await page.type(inputSelector, messageToSend);
            const submitSelector = 'button[type="submit"], input[type="submit"]';
            await page.waitForSelector(submitSelector);
            await page.click(submitSelector);

            
        } catch (error) {
            console.error(error.message);
        }

       
        await new Promise(r => setTimeout(r, 5000));
    }
})();
