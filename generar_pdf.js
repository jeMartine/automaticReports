const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    await page.goto(`file://${__dirname}/vista/index.html`, { waitUntil: 'networkidle0' });

    // Cargar el contenido CSS
    const cssContent = fs.readFileSync('./vista/style.css', 'utf8');
    await page.addStyleTag({ content: cssContent });

    // Esperar a que se cargue el JavaScript y renderice el contenido
    await page.waitForTimeout(1000); // Esperar 1 segundo para asegurarse de que el contenido se renderice

    // Generar el PDF
    await page.pdf({ path: 'prueba.pdf', format: 'A4' });

    await browser.close();
})();
