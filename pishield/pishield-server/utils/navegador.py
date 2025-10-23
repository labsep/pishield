from playwright.sync_api import sync_playwright

class Navegador:
    def __init__(self, timeout=10000):
        self.p = sync_playwright().start()

        self.browser = self.p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-setuid-sandbox"
            ]
        )

        self.page = self.browser.new_page()

        self.timeout = timeout

    def pesquisar(self, url):
        self.page.goto(url, timeout=self.timeout)

        resultado = self.page.inner_text("body")
        print(resultado)

        if not resultado.strip():
            self.page.goto(url, wait_until='domcontentloaded', timeout=self.timeout)

            resultado = self.page.evaluate("body")

        return resultado
    
    def close(self):
        self.browser.close()
        self.p.stop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()