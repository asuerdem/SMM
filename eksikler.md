# Durum

1. Şu an elimizde düzgün çalışan Independent, Guardian, Wired, Mirror, Dailymailve People's China gazeteleri var. Ayrıca Türkiye'den Hürriyet düzgün çalışıyor.

2. Independent, Guardian ve Wired'ı MongoDB ile entegre ettim. Artık ne çekersek mongo'ya yazıyor.

3. monitoringscience.com'u yayına aldım. Linode'a LAMPP kurulumu yapıp gerekli ayarlarla host edecek hale getirdim. Yazdığınız Shiny Dashboard server'da açık olduğu süsrece siteden tıklayınca açılıyor ama eksiklerimiz var:

# Eksikler
## Scraper'lar
1. Cloud makinede crontab kullanarak SMM/1_Crawler/2_weeklycrawler/commands/daily.sh dosyasını her sabah 9da çalışacak şekilde ayarladım. İçinde Independent ve Guardian var. Bir eksik var, henüz çözemedim. İlk fırsatta halledeceğim.

2. Dailymail, Mirror ve People's China'nın günlük scrape eden versiyonlarını yazmadım. Onları da yazıp daily.sh dosyasına ekleyerek çalıştıracağım.

3. Telegraph'ın da scraper'ı mevcut ancak hatırladığım kadarıyla arşivleri 2 sene öncesine kadar açık tutuyorlar. 2 senelik periodu paylaşmıyorlar. Kontrol edilecek.

## Monitoringscience ve Dashboard
1. monitoringscience.com Dashboard'u kendi içinde değil sanki başka siteye bağlanır gibi çalıştırıyor. Yani sitede App'e basınca http://139.162.209.41:8787/p/8989'a yönleniyor. Şu anki hali ile çalışabilmesi için bizim dashboard'un açık olması lazım. Bunu yine crontab ile sağlayabilir yani belli bir zaman aralığında açık olup olmadığını kontrol et, açık değilse aç gibi bir bash kodu yazıp yapabiliriz.

2. Dashboard'un başka bir siteden gibi çekilmesi çok da düzgün bir yol değil, siteye entegre edilmesi lazım. iframe kullanarak wordpress içine eklemiştim ancak chrome secure (https) olmayan siteleri iframe olarak başka bir sayfa içine eklenince göstermiyor. Daha iyi bir yol, Dashboard'u local host'ta gösterip (127.0.0.1:8989 mesela) sitenin içine bir şekilde eklemek. Bunun nasıl yapılacağından emin değilim. Daha da iyi bir yol mutlaka vardır. Bilen varsa yardım etsin.

3. Araştırdığım kadarıyla Python'un django modülü R Shiny'nin görevini üstleniyor (daha doğrusu Shiny Django'nun) ancak Django çok profesyonel ve karmaşık. Bu yaptığımızı bir ara Django ile baştan yapar isek o zaman sitede düzgün bir şekilde yayınlayabiliriz.

4. Monitoringscience.com'a düzgün bir tema giydirilecek. Onu ben Türkiyeye dönünce halledeceğim.

## R, Mongo ve Dashboard bağlantısı
1. Şu an dashboard dışarıdan eklenen bir veri ile çalışıyor. Ancak yakında otomatik çekilen haber verileri ile de çalışabilir. Bu yüzden öncelikle R'dan Mongo'ya bağlanıp sağlıklı bir şekilde veriyi çekmenin ve şu an olduğu gibi bir data.frame haline getirmenin yolunu bulmamız lazım. Rmongo paketi bu işi yapıyor. pymongo gibi rahat değil kullanımı. Üzerinde biraz uğraşacağız.

2. Dashboard'u bu yeni özellik ile etkinleştirmemiz gerekiyor. Yani arayüze farklı bir tuş ekleyip otomatize edeceğiz.

## Backup

1. Bir arkadaştan öğrendiğim kadarı ile Dockers diye bir uygulama ile linux sistemini olduğu gibi yedekleyebiliyormuşuz ve bir problem olursa Docker'ı kullanarak eski haline getirebiliyormuşuz. Diğer Backuplardan falan daha iyi sanırım. Kurulumunun yapılması lazım.

2. Scrape edilen arşivin de backup'ının alınması lazım ve bunun crontaba eklenen bir kod ile otomatik olarak local bir hard disc'e gönderilmesi lazım.

## Elasticsearch
1. Şu an Mongo bizim işimizi kısmen görüyor ancak elasticsearch bizim işler için daha uygun. Öncelikle elasticsearch ile Mongo gibi çalışabiliyor muyuz, syntax farklılıkları neler çözmemiz lazım.

2. Elasticsearch'ü yükleyip mongo ile entegre etmek ya da Mongo'yu tamamen silip scraper'ları elasticsearch ile bağlamamız gerekiyor.

3. Elasticsearch'ün metin sorgusunda daha iyi olduğu noktalarından bahsediyorlar. Onların ne olduğunu öğrenmemiz lazım.
