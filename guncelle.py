from selenium import webdriver
import requests, zipfile, io,sys,time,re




def extract_version():
    """bilgisayrda yüklü olan chrome browser versiyonunu alır"""
    try:
        stream = os.popen('reg query "HKLM\\SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Google Chrome"')
        output = stream.read()
        version = re.findall("\d{1,3}\.\d{1,3}\.\d{1,5}",output)[1]
        return version
    except Exception as e:
        print(f"Bilgisayarda yüklü chrome bilgisi alınamıyor. Hata: {e}")
    
def chrome_indir():
    try:
        guncel_chromedriver = requests.get(f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{str(extract_version())}").text
        r = requests.get(f"https://chromedriver.storage.googleapis.com/{guncel_chromedriver}/chromedriver_win32.zip")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall()
    except Exception as e:
        print(f"Chrome güncellenemedi. Hata kodu: {e}")
        sys.exit(1)
        time(5)

        

def chrome_kontrol():
    try:
        options = webdriver.ChromeOptions()
        options.headless = bool(False)
        driver = webdriver.Chrome(options=options)
        driver.close()
        print("Chrome Güncel.")
    except Exception as e:
        try:
            if 'executable needs to be in PATH.' in e.msg:
                print("Chrome Driver Dosyası bulunamadı.Şimdi otomatik olarak indirelecek.")
                chrome_indir()
            if 'This version of ChromeDriver' in e.msg:
                print("Chrome Driver güncel değil. Şimdi otomatik olarak güncellenecek.")
                chrome_indir()
        except AttributeError:
            print("Chrome Driver yok. Şimdi otomatik olarak indirilecek.")
            chrome_indir()
        print("Chrome Güncellendi.")
        
        
chrome_kontrol()
