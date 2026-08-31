# -*- coding: utf-8 -*-
"""Modül 9 — Routing & Navigation.

Üretim:
    python build_mockup.py 09 main   --selector ".shell" --width 1060 --height 760
    python build_mockup.py 09 detail --html detail.html --selector ".shell" --width 1060 --height 760
    python build_mockup.py 09 denied --html denied.html --selector ".shell" --width 1060 --height 760
    python build_module.py 09
    python build_toc.py
"""
from components import (C, anti, callout, code, divider, h3, lesson_close,
                        lesson_open, p, quiz, recall, shot, table, takeaways,
                        tree)

MODULE_NO = 9
MODULE_TITLE = "Routing & Navigation"

LESSONS = [
    ("m9l1", "Ders 9.1 — Temel Routing"),
    ("m9l2", "Ders 9.2 — Route Parametreleri & Input Binding"),
    ("m9l3", "Ders 9.3 — Functional Guards"),
    ("m9l4", "Ders 9.4 — Functional Resolvers"),
    ("m9l5", "Ders 9.5 — Lazy Loading Rotalar"),
    ("m9l6", "Ders 9.6 — İç İçe Rotalar"),
    ("m9proje", "Mini Proje: Rol Tabanlı Yönetim Paneli"),
    ("m9ozet", "Modül 9 Özeti"),
]


# ---------------------------------------------------------------------------
# Kapak
# ---------------------------------------------------------------------------
def _divider() -> str:
    return divider(
        number=MODULE_NO,
        title=MODULE_TITLE,
        level="Gelişim · Junior → Mid-Level",
        objectives=[
            "Rotaların nasıl tanımlandığını, eşleştiğini ve nasıl gezinildiğini",
            "URL'deki parametreleri " + C("input()") + " ile doğrudan component'e almayı",
            "Guard'larla gezinmeyi durdurmayı, resolver'larla veriyi önden hazırlamayı",
            "Rotaları tembel (lazy) yükleyerek ilk açılışı hızlandırmayı",
            "İç içe rotalarla sabit bir kabuk (sidebar) kurmayı",
        ],
        toc=[
            ("#m9l1", "9.1 Temel Routing"),
            ("#m9l2", "9.2 Route Parametreleri & Input Binding"),
            ("#m9l3", "9.3 Functional Guards"),
            ("#m9l4", "9.4 Functional Resolvers"),
            ("#m9l5", "9.5 Lazy Loading Rotalar"),
            ("#m9l6", "9.6 İç İçe Rotalar"),
            ("#m9proje", "Mini Proje: Rol Tabanlı Yönetim Paneli"),
            ("#m9ozet", "Özet"),
        ],
    )


# ---------------------------------------------------------------------------
# 9.1 Temel Routing  (çekirdek konu — derin)
# ---------------------------------------------------------------------------
def _lesson_1() -> str:
    h = [lesson_open("9.1", "Temel Routing", "m9l1", order=1)]

    h.append(p(
        "Modül 8'in sonunda uygulaman dış dünyayla konuşuyordu: veriyi çekiyor, "
        "yazıyor, hatayı yönetiyordu. Ama hepsi <strong>tek bir ekranda</strong> "
        "oluyordu. Bu modülde uygulamana <strong>sayfa</strong> kavramını "
        "kazandırıyoruz."))

    h.append(recall([
        "Modül 5: Durumu " + C("signal()") + " içinde tutmak. Routing, durumun bir "
        "kısmını signal yerine <strong>URL'de</strong> tutmanın yoludur.",
        "Modül 7: " + C("@Service()") + " + " + C("inject()") + ". Guard ve "
        "resolver'lar da " + C("inject()") + " kullanır.",
        "Modül 8: " + C("httpResource") + " ile veri çekmek. Bu modülde veriyi "
        "<strong>hangi ürünün</strong> çekileceğini URL belirleyecek.",
    ]))

    h.append(h3("Nedir?"))
    h.append(p(
        "<strong>Router, adres çubuğundaki URL'e bakıp hangi component'i "
        "göstereceğine karar eden yapıdır.</strong> Sunucuya yeni bir sayfa "
        "istemez; aynı sayfa içinde ekranı değiştirir, ama URL'i de günceller."))

    h.append(h3("Neden var? “Signal ile ekran değiştirsem olmaz mı?”"))
    h.append(p(
        "Teknik olarak olur: bir " + C("currentPage = signal('list')") + " tutup "
        "şablonda " + C("@switch") + " ile ekran değiştirebilirsin. Ama üç şeyi "
        "kaybedersin:"))
    h.append(table(["Kaybettiğin şey", "Neden önemli"], [
        ["<strong>Paylaşılabilir adres</strong>",
         "Kullanıcı bir ürünün linkini arkadaşına gönderemez; herkes hep ana ekranda açar."],
        ["<strong>Geri / ileri tuşu</strong>",
         "Tarayıcının geri tuşu uygulamandan tamamen çıkar — kullanıcı için kırık his."],
        ["<strong>Yer imi ve yenileme</strong>",
         C("F5") + "'e basınca bulunduğun yerde kalman gerekir; signal'de tutulan ekran sıfırlanır."],
    ]))
    h.append(p(
        "Kural şu: <strong>kullanıcının geri tuşuyla dönmek isteyeceği ya da "
        "linkini paylaşmak isteyeceği her durum URL'e aittir.</strong> Gerisi "
        "signal'de kalır."))

    h.append(h3("Nasıl? Üç parça"))
    h.append(p("Routing üç parçadan oluşur ve üçü de olmadan çalışmaz:"))

    h.append(p("<strong>1) Rota tablosu</strong> — hangi yol hangi component:"))
    h.append(code('''// app.routes.ts
import { Routes } from '@angular/router';
import { ProductList } from './pages/product-list/product-list';
import { ProductDetail } from './pages/product-detail/product-detail';
import { NotFound } from './pages/not-found/not-found';

export const routes: Routes = [
  { path: '', redirectTo: 'products', pathMatch: 'full' },
  { path: 'products', component: ProductList, title: 'Ürünler' },
  { path: 'products/:id', component: ProductDetail },
  { path: '**', component: NotFound },        // en SONDA olmalı
];''', "typescript"))

    h.append(p("<strong>2) Router'ı sağlamak</strong> — uygulama yapılandırmasında:"))
    h.append(code('''// app.config.ts
import { provideRouter, withComponentInputBinding } from '@angular/router';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes, withComponentInputBinding()),
    provideHttpClient(withInterceptors([baseUrlInterceptor])),
  ],
};''', "typescript"))
    h.append(p(
        C("withComponentInputBinding()") + " şu an gereksiz görünebilir; 9.2'de "
        "bunun sayesinde URL parametrelerinin doğrudan " + C("input()") +
        "'lara aktığını göreceğiz. Baştan ekle."))

    h.append(p("<strong>3) Çıkış noktası ve bağlantılar</strong> — şablonda:"))
    h.append(code('''@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <nav>
      <a routerLink="/products" routerLinkActive="active">Ürünler</a>
      <a routerLink="/about" routerLinkActive="active">Hakkında</a>
    </nav>

    <!-- Eşleşen component TAM BURAYA basılır -->
    <router-outlet />
  `,
})
export class App {}''', "typescript"))

    h.append(callout("warn", C("routerLink") + " mi " + C("href") + " mi?",
                     "<p>" + C('<a href="/products">') + " tarayıcıya <strong>“bu adresi "
                     "sunucudan yeniden iste”</strong> der: sayfa baştan yüklenir, "
                     "uygulamanın bütün durumu sıfırlanır, kullanıcı beyaz ekran görür. "
                     + C("routerLink") + " ise Router'a haber verir; ekran değişir ama "
                     "sayfa yenilenmez.</p>"))

    h.append(h3("Yol yazımları"))
    h.append(table(["Yazım", "Anlamı"], [
        [C("path: ''"), "Kök adres. Genelde bir " + C("redirectTo") + " ile eşleşir."],
        [C("path: 'products'"), "Sabit yol: " + C("/products")],
        [C("path: 'products/:id'"), "Parametreli yol: " + C("/products/42") + " → " + C("id = '42'")],
        [C("path: '**'"), "Hiçbiri tutmazsa (404). <strong>Dizinin en sonunda</strong> olmalı."],
        [C("redirectTo: 'products'"), "Yönlendirme. Boş yolda " + C("pathMatch: 'full'") + " ile birlikte."],
        [C("title: 'Ürünler'"), "Sekme başlığı. Router bunu otomatik " + C("document.title") + "'a yazar."],
    ]))

    h.append(callout("warn", C("pathMatch: 'full'") + " neden şart?",
                     "<p>Yol eşleştirme varsayılan olarak <strong>“prefix”</strong> "
                     "modundadır: " + C("path: ''") + " her URL'in başında bulunduğu "
                     "için <strong>her adresle eşleşir</strong>. Yönlendirmen sonsuz "
                     "döngüye girer ya da hiçbir sayfaya ulaşamazsın. " + C("'full'") +
                     " ise “URL'in tamamı boş olsun” der.</p><p>Dolu yollarda "
                     "(" + C("'products'") + ") gerekmez.</p>"))

    h.append(h3("Koddan gezinme"))
    h.append(p(
        "Şablondan " + C("routerLink") + ", koddan " + C("Router") + ". Kaydetme "
        "bittikten sonra listeye dönmek gibi durumlarda ikincisi gerekir:"))
    h.append(code('''import { inject } from '@angular/core';
import { Router } from '@angular/router';

export class ProductCreate {
  private readonly router = inject(Router);
  private readonly productService = inject(ProductService);

  save(): void {
    this.productService.add(/* ... */).subscribe(() => {
      // Dizi biçimi: her eleman bir yol parçası
      this.router.navigate(['/products']);
    });
  }
}''', "typescript"))
    h.append(p(
        "Dizi biçimini tercih et: " + C("['/products', id]") + " parçaları senin "
        "yerine güvenli biçimde birleştirir. Metin birleştirmede (" +
        C("'/products/' + id") + ") özel karakterler seni yakar."))

    h.append(quiz(
        ["Routing üç parçadan oluşur — hangileri?",
         C("pathMatch: 'full'") + " neden yalnızca boş yolda gerekir?",
         C("'**'") + " rotası neden dizinin sonunda olmalı?",
         "Şablondan ve koddan gezinme sırasıyla neyle yapılır?"],
        ["Rota tablosu (" + C("routes") + "), " + C("provideRouter()") + " ve "
         + C("<router-outlet />") + " (+ " + C("routerLink") + ").",
         "Eşleştirme varsayılan olarak “prefix”tir; boş yol o modda <strong>her</strong> "
         "URL ile eşleşir.",
         "Router yukarıdan aşağıya <strong>ilk eşleşeni</strong> seçer; " + C("'**'")
         + " her şeyle eşleştiği için kendinden sonrakileri gölgeler.",
         C("routerLink") + " ve " + C("inject(Router).navigate([...])") + "."],
    ))
    h.append(anti([
        "<strong>" + C("href") + " kullanmak.</strong> Tam sayfa yeniler, uygulama "
        "durumu sıfırlanır. Uygulama içi her bağlantı " + C("routerLink") + ".",
        "<strong>" + C('routerLink="/products/{{ id }}"') + " yazmak.</strong> "
        "Bu metin enterpolasyonudur ve karışıklık üretir; parametreli gezinmede "
        + C('''[routerLink]="['/products', id]"''') + " kullan.",
        "<strong>" + C("<router-outlet />") + "'i unutmak.</strong> Rota eşleşir, "
        "hata da almazsın — ekranda hiçbir şey görünmez.",
        "<strong>" + C("'**'") + "'ı listenin başına koymak.</strong> Bütün "
        "uygulaman 404 sayfası olur.",
    ]))
    h.append(takeaways([
        "Router = URL → component eşleştiricisi; SPA'ya geri tuşu ve "
        "paylaşılabilir adres kazandırır.",
        "Üç parça: " + C("routes") + " + " + C("provideRouter()") + " + "
        + C("<router-outlet />") + ".",
        "Kullanıcının linkini paylaşacağı ya da geri tuşuyla döneceği durum "
        "URL'e, gerisi signal'e ait.",
        "Boş yolda " + C("pathMatch: 'full'") + ", " + C("'**'") + " en sonda.",
        "Koddan gezinme " + C("router.navigate([...])") + " — dizi biçimiyle.",
    ]))

    h.append(lesson_close())
    return "".join(h)


# ---------------------------------------------------------------------------
# 9.2 Route Parametreleri & Component Input Binding  (çekirdek konu — derin)
# ---------------------------------------------------------------------------
def _lesson_2() -> str:
    h = [lesson_open("9.2", "Route Parametreleri & Component Input Binding", "m9l2", order=2)]

    h.append(p(
        "Rota tablosunu kurdun. Şimdi asıl soru: " + C("/products/42") + " "
        "adresindeki <strong>42</strong> component'in içine nasıl girecek?"))

    h.append(h3("Nedir? URL'in dört bilgi kaynağı"))
    h.append(p("Router bir rotayı aktive ederken elinde dört ayrı bilgi kümesi olur:"))
    h.append(table(["Kaynak", "Örnek", "Ne zaman kullanılır"], [
        ["<strong>Yol parametresi</strong> (path param)", C("/products/42") + " → " + C("id"),
         "Kaynağı <strong>tanımlayan</strong> bilgi. Onsuz sayfa anlamsız."],
        ["<strong>Sorgu parametresi</strong> (query param)", C("?q=kahve&page=2"),
         "Sayfayı <strong>ayarlayan</strong> bilgi: arama, sayfa, sıralama, filtre."],
        ["<strong>Statik veri</strong>", C("data: { role: 'admin' }"),
         "Rotaya sabitlenmiş yapılandırma."],
        ["<strong>Resolver verisi</strong>", C("resolve: { product }"),
         "Rota açılmadan önce çözülmüş veri (9.4)."],
    ]))

    h.append(h3("Neden ikisi ayrı? (Sık karıştırılır)"))
    h.append(p(
        "Ölçüt basit: <strong>o bilgi olmadan sayfa var olabiliyor mu?</strong> "
        "Ürün detayı " + C("id") + " olmadan var olamaz → yol parametresi. Ürün "
        "listesi arama terimi olmadan gayet iyi çalışır, terim sadece görünümü "
        "daraltır → sorgu parametresi."))

    h.append(h3("Nasıl? " + C("input()") + " ile doğrudan bağlama"))
    h.append(p(
        C("provideRouter(routes, withComponentInputBinding())") + " eklendiğinde "
        "Router, bu dört kaynaktaki değerleri <strong>aynı ada sahip</strong> "
        + C("input()") + "'lara kendiliğinden yazar. Ek bir abonelik ya da kurulum "
        "kodu yazmazsın:"))
    h.append(code('''// Rota:  { path: 'products/:id', component: ProductDetail }

@Component({ /* ... */ })
export class ProductDetail {
  // Ada dikkat: rotadaki ':id' ile birebir aynı olmalı
  readonly id = input.required<string>();

  private readonly productService = inject(ProductService);

  // id() değişince URL değişir, httpResource kendini yeniler (Modül 8)
  readonly product = httpResource<Product>(() => `products/${this.id()}`);
}''', "typescript"))

    h.append(callout("warn", "Yol parametreleri <strong>her zaman metindir</strong>",
                     "<p>" + C("input.required<number>()") + " yazsan bile URL'den gelen "
                     "değer " + C("'42'") + " (string) olur. TypeScript bunu derlerken "
                     "yakalayamaz, çünkü değeri Router çalışma anında yazar. Sonuç: "
                     + C("id === 42") + " hep " + C("false") + ", " + C("id + 1") +
                     " ise " + C("'421'") + ".</p>"
                     "<p>Çözüm sayı gerekiyorsa dönüştürücü kullanmak:</p>"))
    h.append(code('''import { input, numberAttribute } from '@angular/core';

readonly id = input.required({ transform: numberAttribute });   // number
readonly page = input(1, { transform: numberAttribute });       // varsayılan 1''', "typescript"))

    h.append(h3("Sorgu parametreleri"))
    h.append(p("Aynı mekanizma sorgu parametreleri için de çalışır:"))
    h.append(code('''// URL:  /products?q=kahve&page=2

export class ProductList {
  readonly q = input('');                                    // arama terimi
  readonly page = input(1, { transform: numberAttribute });  // sayfa
}''', "typescript"))
    h.append(p("Şablondan sorgu parametresiyle gezinmek:"))
    h.append(code('''<!-- Sadece sayfayı değiştir, aramayı KORU -->
<a [routerLink]="['/products']"
   [queryParams]="{ page: page() + 1 }"
   queryParamsHandling="merge">Sonraki</a>''', "html"))
    h.append(table([C("queryParamsHandling"), "Davranış"], [
        [C("'merge'"), "Yeni parametreleri mevcutlarla birleştirir. Sayfalama/filtre için doğru seçim."],
        [C("'preserve'"), "Mevcutları aynen korur, yenileri yok sayar."],
        [C("'replace'"), "<strong>Varsayılan.</strong> Mevcutları siler, yalnızca yenileri kalır."],
    ]))
    h.append(p(
        "Varsayılanın " + C("'replace'") + " olduğunu unutma: sayfa değiştiren bir "
        "bağlantıya " + C("queryParamsHandling") + " yazmazsan kullanıcının arama "
        "terimi sessizce kaybolur."))

    h.append(h3("Mutfak detayı: aynı rotada parametre değişirse ne olur?"))
    h.append(p(
        C("/products/1") + " sayfasındayken " + C("/products/2") + "'ye gidersen "
        "Router component'i <strong>yeniden oluşturmaz</strong> — aynı component "
        "örneğini kullanır, yalnızca " + C("input") + " değerini günceller. Bu "
        "bilinçli bir tasarım (performans), ama iki sonucu var:"))
    h.append(table(["Yaklaşım", "Ne olur?"], [
        [C("ngOnInit") + " içinde veriyi çekmek",
         "<strong>Bir daha çalışmaz.</strong> Ekranda hâlâ 1 numaralı ürün durur."],
        [C("httpResource(() => `products/${id()}`)"),
         "<strong>Kendiliğinden yenilenir.</strong> " + C("id()") + " bir signal olduğu için."],
    ]))
    h.append(p(
        "Modül 5'ten beri kurduğumuz signal alışkanlığı burada bedavaya kazandırıyor: "
        + C("input()") + " zaten bir signal, " + C("httpResource") + " onu okuduğu "
        "için bağımlılık kurulmuş oluyor."))

    h.append(callout("note", "Eşleşmeyen " + C("input") + " ne olur?",
                     "<p>Bir " + C("input") + "'a karşılık gelen anahtar URL'de yoksa "
                     "Router ona " + C("undefined") + " yazar — eski değer <strong>"
                     "kalmaz</strong>. Bu, kullanıcı " + C("?q=kahve") + "'yi silince "
                     "ekranda eski aramanın asılı kalmasını engeller. Bu yüzden sorgu "
                     "parametresi bağlayan input'lara <strong>varsayılan değer ver</strong>: "
                     + C("input('')") + ", " + C("input(1, { transform: numberAttribute })") +
                     ".</p>"))

    h.append(callout("info", "Çakışma olursa kim kazanır?",
                     "<p>Aynı ada sahip birden çok kaynak varsa öncelik sırası şudur "
                     "(zayıftan güçlüye): <strong>sorgu parametresi → yol parametresi → "
                     "statik " + C("data") + " → resolver verisi</strong>. Yani resolver "
                     "her zaman son sözü söyler.</p>"))

    h.append(quiz(
        ["Bir bilginin yol mu sorgu parametresi mi olduğuna nasıl karar verirsin?",
         C("id = input.required<number>()") + " yazdın ama karşılaştırmalar tutmuyor. Neden?",
         "Sayfa numarasını değiştiren bağlantıda arama terimi kayboluyor. Eksik olan ne?",
         C("/products/1") + "'den " + C("/products/2") + "'ye geçince veri neden tazelenmedi?"],
        ["“O bilgi olmadan sayfa var olabilir mi?” Olamıyorsa yol, olabiliyorsa sorgu parametresi.",
         "URL'den gelen değer <strong>her zaman string</strong>'dir; tip yalnızca "
         "derleme zamanı iddiasıdır. " + C("transform: numberAttribute") + " kullan.",
         C("queryParamsHandling=\"merge\"") + ". Varsayılan " + C("'replace'") + " "
         "diğer parametreleri siler.",
         "Veriyi " + C("ngOnInit") + "'te çektin. Component yeniden oluşmaz; "
         + C("httpResource") + " gibi signal okuyan bir kaynak kullan."],
    ))
    h.append(anti([
        "<strong>URL parametresini sayı sanmak.</strong> Hep string gelir; "
        + C("numberAttribute") + " ile dönüştür.",
        "<strong>" + C("input") + " adını rotadaki parametreden farklı yazmak.</strong> "
        "Hata almazsın, değer sessizce " + C("undefined") + " kalır.",
        "<strong>" + C("withComponentInputBinding()") + "'i eklemeyi unutmak.</strong> "
        "Aynı sessiz " + C("undefined") + ": rota çalışır, parametre gelmez.",
        "<strong>Filtreyi yalnızca signal'de tutmak.</strong> Kullanıcı filtrelediği "
        "listenin linkini paylaşamaz, " + C("F5") + " her şeyi sıfırlar.",
    ]))
    h.append(takeaways([
        "Yol parametresi kaynağı <strong>tanımlar</strong>, sorgu parametresi "
        "görünümü <strong>ayarlar</strong>.",
        C("withComponentInputBinding()") + " + aynı adlı " + C("input()") +
        " = ek kod olmadan bağlama.",
        "Gelen değer her zaman string; sayı için " + C("transform: numberAttribute") + ".",
        "Aynı rotada parametre değişince component yeniden oluşmaz — signal "
        "tabanlı kaynak (" + C("httpResource") + ") kullan.",
        C("queryParamsHandling=\"merge\"") + " olmadan diğer parametreler silinir.",
    ]))

    h.append(lesson_close())
    return "".join(h)


# ---------------------------------------------------------------------------
# 9.3 Functional Guards  (çekirdek konu — derin)
# ---------------------------------------------------------------------------
def _lesson_3() -> str:
    h = [lesson_open("9.3", "Functional Guards — Gezinmeyi Denetlemek", "m9l3", order=3)]

    h.append(p(
        "Rotalar artık çalışıyor. Ama " + C("/admin") + " adresini adres çubuğuna "
        "yazan herkes oraya girebiliyor. Guard'lar bu kapıyı tutan bekçilerdir."))

    h.append(h3("Nedir?"))
    h.append(p(
        "<strong>Guard, bir gezinme başladığında çalışan ve “bu gezinme devam "
        "etsin mi?” sorusunu yanıtlayan bir fonksiyondur.</strong> Sıradan bir "
        "fonksiyondur; içinde " + C("inject()") + " kullanabilirsin."))

    h.append(h3("Dört tür guard"))
    h.append(table(["Tür", "Ne zaman çalışır", "Tipik iş"], [
        [C("canActivate"), "Rota aktive edilmeden hemen önce", "Giriş yapılmış mı, rolü yeterli mi"],
        [C("canActivateChild"), "Çocuk rotalar aktive edilmeden önce", "Bir bölümün tamamını tek yerden korumak"],
        [C("canMatch"), "Rota <strong>eşleştirilirken</strong>", "Rotanın hiç eşleşmemesini sağlamak (aşağıda)"],
        [C("canDeactivate"), "Rotadan <strong>çıkarken</strong>", "“Kaydedilmemiş değişiklik var” uyarısı"],
    ]))

    h.append(h3("Nasıl? En yalın guard"))
    h.append(code('''// guards/admin-guard.ts
import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '@app/services/auth-service';

export const adminGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);

  if (auth.role() === 'admin') {
    return true;
  }

  // false yerine YÖNLENDİRME döndür — kullanıcı neden giremediğini görsün
  return router.createUrlTree(['/unauthorized']);
};''', "typescript"))
    h.append(code('''// app.routes.ts
{ path: 'admin/new-product', component: ProductCreate, canActivate: [adminGuard] },''', "typescript"))

    h.append(h3("Guard ne döndürebilir?"))
    h.append(table(["Dönüş", "Sonuç"], [
        [C("true"), "Gezinme devam eder."],
        [C("false"), "Gezinme <strong>iptal edilir</strong>. Kullanıcı bulunduğu sayfada kalır."],
        [C("UrlTree"), "Gezinme iptal edilir ve bu adrese <strong>yönlendirilir</strong>."],
        [C("RedirectCommand"), "Yönlendirme + ek seçenek (ör. geçmişte iz bırakmadan)."],
        [C("Observable") + " / " + C("Promise"), "Yukarıdakilerin asenkron hâli; Router bekler."],
    ]))
    h.append(callout("tip", C("false") + " mi, " + C("UrlTree") + " mi?",
                     "<p>" + C("false") + " döndürmek kullanıcıyı olduğu yerde bırakır: "
                     "tıklar, hiçbir şey olmaz, nedenini anlamaz. Bir sayfa yetki "
                     "istiyorsa " + C("router.createUrlTree(['/unauthorized'])") +
                     " ile açıklayıcı bir ekrana gönder. " + C("false") + "'ı asıl "
                     + C("canDeactivate") + "'te (kullanıcı “Hayır, kalmak istiyorum” "
                     "dediğinde) kullanırsın.</p>"))

    h.append(h3(C("canActivate") + " ile " + C("canMatch") + " farkı"))
    h.append(p(
        "İkisi de erişimi engeller ama <strong>farklı anda</strong> çalışır ve bu "
        "fark önemlidir:"))
    h.append(table(["", C("canActivate"), C("canMatch")], [
        ["Ne zaman", "Rota eşleşti, aktive edilecek", "Rota eşleştirilirken"],
        ["Engellerse", "Gezinme durur / yönlenir", "Rota <strong>hiç eşleşmemiş sayılır</strong>, arama devam eder"],
        ["Lazy chunk", "İndirilmiş olur", "<strong>İndirilmez</strong>"],
        ["Kullanımı", "“Girebilir mi?”", "“Bu rota bu kullanıcı için var mı?”"],
    ]))
    h.append(p(
        C("canMatch") + " rota eşleştirmesini etkilediği için şuna izin verir: "
        "<strong>aynı adres, role göre farklı component.</strong>"))
    h.append(code('''export const routes: Routes = [
  // Router yukarıdan aşağıya bakar. adminGuard geçerse ilki eşleşir...
  { path: 'reports', component: AdminReports, canMatch: [adminGuard] },
  // ...geçmezse ilk rota hiç yokmuş gibi davranılır ve bu eşleşir
  { path: 'reports', component: BasicReports },
];''', "typescript"))

    h.append(h3(C("canDeactivate") + " — çıkışı tutmak"))
    h.append(p(
        "Diğerlerinden farklı olarak bu guard <strong>component örneğini</strong> "
        "alır; böylece bileşenin durumuna bakabilir:"))
    h.append(code('''// guards/unsaved-changes-guard.ts
export interface HasUnsavedChanges {
  hasUnsavedChanges(): boolean;
}

export const unsavedChangesGuard: CanDeactivateFn<HasUnsavedChanges> = (component) => {
  if (!component.hasUnsavedChanges()) {
    return true;
  }
  return confirm('Kaydedilmemiş değişiklikler var. Yine de çıkmak istiyor musun?');
};''', "typescript"))

    h.append(callout("warn", "Guard içinde " + C("inject()") + " neden çalışıyor?",
                     "<p>Guard'lar sıradan fonksiyonlardır; " + C("inject()") + " ise "
                     "yalnızca “injection context” denen anlarda çalışır. Router, "
                     "guard'ı bilinçli olarak bu bağlamda çağırır — o yüzden "
                     "<strong>fonksiyonun ilk satırlarında</strong> " + C("inject()") +
                     " serbesttir.</p><p>Ama " + C("setTimeout") + " ya da bir "
                     + C("subscribe") + " geri çağrımının <strong>içinde</strong> "
                     + C("inject()") + " çağırırsan bağlam çoktan kapanmıştır ve "
                     "hata alırsın. Kuralı basit tut: <strong>bütün " + C("inject()") +
                     " çağrılarını en üstte yap</strong>, sonra mantığı yaz.</p>"))

    h.append(quiz(
        ["Guard " + C("false") + " döndürdüğünde kullanıcı nerede kalır?",
         "Lazy yüklenen bir yönetici bölümünü korurken hangi guard'ı seçersin, neden?",
         C("canDeactivate") + "'i diğerlerinden ayıran nedir?",
         "Guard yetkiyi denetliyorsa API'de ayrıca kontrol gerekir mi?"],
        ["Bulunduğu sayfada — hiçbir şey olmamış gibi. Nedenini göstermek için "
         + C("createUrlTree([...])") + " ile yönlendir.",
         C("canMatch") + ": rota eşleşmediği için lazy chunk <strong>hiç indirilmez</strong>.",
         "Component örneğini parametre olarak alır; bileşenin durumuna bakabilir.",
         "<strong>Kesinlikle evet.</strong> Guard bir arayüz kolaylığıdır; tarayıcıda "
         "çalışan her kod değiştirilebilir. Yetki denetiminin gerçeği sunucudadır."],
    ))
    h.append(anti([
        "<strong>Guard'ı güvenlik sanmak.</strong> Guard yalnızca arayüzü düzenler; "
        "gerçek denetim sunucuda yapılır.",
        "<strong>Guard içinde veri çekmek.</strong> Guard “girebilir mi?” sorusunu "
        "yanıtlar; veri hazırlamak resolver'ın işidir (9.4).",
        "<strong>" + C("inject()") + "'i geri çağrımın içinde kullanmak.</strong> "
        "Injection context kapanmıştır; çağrıları fonksiyonun en üstünde yap.",
        "<strong>Yalnızca " + C("false") + " döndürmek.</strong> Kullanıcı tıklar, "
        "hiçbir şey olmaz, nedenini anlamaz.",
    ]))
    h.append(takeaways([
        "Guard = gezinmeyi denetleyen sıradan fonksiyon; içinde " + C("inject()") + " çalışır.",
        C("canActivate") + " girişi, " + C("canMatch") + " eşleşmeyi, "
        + C("canDeactivate") + " çıkışı denetler.",
        C("UrlTree") + " döndürmek " + C("false") + " döndürmekten neredeyse her zaman iyidir.",
        C("canMatch") + " ile aynı adres role göre farklı component'e gidebilir.",
        "Guard arayüz kolaylığıdır — yetkinin gerçeği sunucuda denetlenir.",
    ]))

    h.append(lesson_close())
    return "".join(h)


# ---------------------------------------------------------------------------
# 9.4 Functional Resolvers  (orta derinlik)
# ---------------------------------------------------------------------------
def _lesson_4() -> str:
    h = [lesson_open("9.4", "Functional Resolvers — Veriyi Önden Hazırlamak", "m9l4", order=4)]

    h.append(p(
        "Guard “girebilir mi?” diye sorar. Resolver ise <strong>“girmeden önce "
        "şu veriyi hazırla”</strong> der."))

    h.append(h3("Nedir?"))
    h.append(p(
        "<strong>Resolver, rota aktive edilmeden önce çalışan ve döndürdüğü veri "
        "hazır olana kadar gezinmeyi bekleten bir fonksiyondur.</strong> Component "
        "açıldığında veri çoktan elindedir."))

    h.append(h3("Neden? İki farklı açılış hissi"))
    h.append(table(["Resolver'sız", "Resolver'lı"], [
        ["Sayfa hemen açılır, içerik boştur; iskelet döner, sonra veri gelir.",
         "Kullanıcı bir an bulunduğu sayfada bekler, sonra <strong>dolu</strong> sayfaya geçer."],
        ["Ürün yoksa: sayfa açılır, sonra “bulunamadı” gösterilir.",
         "Ürün yoksa: sayfa <strong>hiç açılmaz</strong>, listeye geri yönlendirilir."],
    ]))
    h.append(p(
        "İkisi de doğrudur; seçim veriye bağlıdır. Küçük ve hızlı bir kayıt için "
        "resolver daha derli toplu bir his verir. Büyük listelerde ise resolver "
        "uygulamayı <strong>donmuş gibi</strong> gösterir — orada iskelet daha iyidir."))

    h.append(h3("Nasıl?"))
    h.append(code('''// resolvers/product-resolver.ts
import { inject } from '@angular/core';
import { ResolveFn, RedirectCommand, Router } from '@angular/router';
import { catchError, of } from 'rxjs';

export const productResolver: ResolveFn<Product | RedirectCommand> = (route) => {
  const productService = inject(ProductService);
  const router = inject(Router);

  const id = Number(route.paramMap.get('id'));

  return productService.getById(id).pipe(
    // Ürün yoksa sayfayı hiç açma, listeye gönder
    catchError(() => of(new RedirectCommand(router.parseUrl('/products')))),
  );
};''', "typescript"))
    h.append(code('''// app.routes.ts
{
  path: 'products/:id',
  component: ProductDetail,
  resolve: { product: productResolver },   // anahtar adı: 'product'
},''', "typescript"))
    h.append(p(
        "Component tarafı 9.2'deki kalıbın aynısı — resolver'daki <strong>anahtar "
        "adıyla</strong> aynı adı taşıyan bir " + C("input") + " yeter:"))
    h.append(code('''export class ProductDetail {
  // resolve: { product: ... } -> input adı da 'product'
  readonly product = input.required<Product>();
}''', "typescript"))
    h.append(p(
        "Dikkat: burada " + C("httpResource") + ", " + C("isLoading") + ", "
        + C("hasValue()") + " kontrolü yok. Veri garanti hazır olduğu için "
        "component sadeleşir. Resolver'ın asıl kazancı budur."))

    h.append(callout("warn", "Mutfak detayı: resolver ne zaman <strong>yeniden</strong> çalışır?",
                     "<p>Varsayılan davranış " + C("paramsChange") + "'dir: resolver "
                     "yalnızca <strong>yol parametresi</strong> değişince yeniden "
                     "çalışır. Sorgu parametresi değişince çalışmaz.</p>"
                     "<p>Yani " + C("?page=2") + "'den " + C("?page=3") + "'e "
                     "geçtiğinde resolver'ın verisi <strong>eski kalır</strong> ve "
                     "bunu fark etmek zordur: hata yok, ekran değişmiyor. Gerekiyorsa "
                     "rotaya " + C("runGuardsAndResolvers: 'paramsOrQueryParamsChange'") +
                     " ekle.</p>"))

    h.append(quiz(
        ["Resolver ile guard arasındaki temel fark nedir?",
         "Resolver kullanınca component'te hangi kodlar gereksizleşir?",
         "Sayfa numarası sorgu parametresiyle değişiyor ama resolver verisi tazelenmiyor. Neden?"],
        ["Guard gezinmeye <strong>izin verir/vermez</strong>; resolver gezinmeden "
         "önce <strong>veri hazırlar</strong>.",
         "Yükleniyor durumu ve " + C("hasValue()") + " korumaları — veri garanti hazırdır.",
         "Varsayılan " + C("paramsChange") + " yalnızca yol parametresini izler; "
         + C("runGuardsAndResolvers: 'paramsOrQueryParamsChange'") + " gerekir."],
    ))
    h.append(anti([
        "<strong>Her veriyi resolver'a taşımak.</strong> Yavaş isteklerde uygulama "
        "donmuş görünür; büyük listeler için " + C("httpResource") + " + iskelet daha iyidir.",
        "<strong>Resolver'da hatayı ele almamak.</strong> İstek patlarsa gezinme "
        "sessizce iptal olur ve kullanıcı hiçbir şey olmamış sanır.",
        "<strong>Resolver anahtarı ile " + C("input") + " adını farklı yazmak.</strong> "
        "Yine sessiz " + C("undefined") + ".",
    ]))
    h.append(takeaways([
        "Resolver = rota açılmadan veriyi hazırlayan fonksiyon; component sadeleşir.",
        "Anahtar adı (" + C("resolve: { product }") + ") ile " + C("input") + " adı aynı olmalı.",
        C("RedirectCommand") + " ile “kayıt yoksa hiç açma, yönlendir” davranışı kurulur.",
        "Varsayılanda yalnızca yol parametresi değişince yeniden çalışır.",
        "Her yerde değil: yavaş/büyük veride iskelet göstermek daha iyi bir histir.",
    ]))

    h.append(lesson_close())
    return "".join(h)


# ---------------------------------------------------------------------------
# 9.5 Lazy Loading  (orta derinlik)
# ---------------------------------------------------------------------------
def _lesson_5() -> str:
    h = [lesson_open("9.5", "Lazy Loading — Rotaları Tembel Yüklemek", "m9l5", order=5)]

    h.append(p(
        "Uygulaman büyüdükçe ilk açılışta indirilen JavaScript de büyür. Kullanıcı "
        "belki hiç girmeyeceği yönetici ekranlarının kodunu da indirir. Lazy "
        "loading bunu düzeltir."))

    h.append(h3("Nedir? Neden?"))
    h.append(p(
        "<strong>Lazy loading, bir rotanın kodunu ancak o rotaya gidildiğinde "
        "indirmektir.</strong> Kazanç ilk açılış süresinde görülür: kullanıcı "
        "gördüğü ekranın kodunu indirir, gerisini indirmez."))

    h.append(h3("Nasıl? İki biçim"))
    h.append(p("<strong>Tek component:</strong> " + C("loadComponent")))
    h.append(code('''{
  path: 'reports',
  loadComponent: () => import('./pages/reports/reports').then((m) => m.Reports),
}''', "typescript"))
    h.append(p("<strong>Bir rota grubu:</strong> " + C("loadChildren")))
    h.append(code('''// app.routes.ts
{
  path: 'admin',
  loadChildren: () => import('./features/admin/admin.routes').then((m) => m.adminRoutes),
}

// features/admin/admin.routes.ts
export const adminRoutes: Routes = [
  { path: '', component: AdminHome },
  { path: 'users', component: AdminUsers },
];''', "typescript"))

    h.append(callout("warn", "Sık yapılan yanlış: üstte " + C("import") + " edip "
                     + C("loadComponent") + " yazmak",
                     "<p>Şunu yazarsan lazy loading <strong>olmaz</strong>:</p>"))
    h.append(code('''import { Reports } from './pages/reports/reports';   // <-- bu satır her şeyi bozar

{ path: 'reports', loadComponent: () => Promise.resolve(Reports) }''', "typescript"))
    h.append(p(
        "Dosyanın en üstündeki " + C("import") + " satırı, o component'i zaten ana "
        "pakete katmıştır. Ayırmayı sağlayan şey <strong>dinamik</strong> "
        + C("import()") + " çağrısıdır. Kural: üstte " + C("import") + " ettiğin "
        "component için " + C("component:") + " kullan; ayırmak istiyorsan "
        "<strong>yalnızca</strong> dinamik " + C("import()") + " yaz."))

    h.append(h3("Guard ile birleşince"))
    h.append(p(
        "9.3'teki fark burada işe yarıyor: " + C("canActivate") + " chunk indikten "
        "sonra çalışır, " + C("canMatch") + " ise indirmeden önce. Yetkisiz "
        "kullanıcıya yönetici kodunu hiç göndermek istemiyorsan " + C("canMatch") +
        " kullan:"))
    h.append(code('''{
  path: 'admin',
  canMatch: [adminGuard],                      // önce bak
  loadChildren: () => import('./features/admin/admin.routes')
    .then((m) => m.adminRoutes),               // sonra indir
}''', "typescript"))

    h.append(h3("Önden yükleme (preloading)"))
    h.append(p(
        "Lazy loading'in bedeli, kullanıcının tıkladığı anda kısa bir bekleme "
        "olmasıdır. Preloading, uygulama açıldıktan <strong>sonra</strong>, boşta "
        "kalan zamanda lazy paketleri arka planda indirir:"))
    h.append(code('''import { provideRouter, withPreloading, PreloadAllModules } from '@angular/router';

provideRouter(routes, withComponentInputBinding(), withPreloading(PreloadAllModules)),''', "typescript"))
    h.append(p(
        "Böylece ilk açılış hızlı kalır <em>ve</em> gezinme anında olur. Yalnızca "
        + C("canMatch") + " ile korunan rotalar bu durumda da indirilmez."))

    h.append(recall([
        "Modül 3: DevTools <strong>Network</strong> sekmesi. Lazy loading'i "
        "gerçekten doğrulamanın tek yolu: rotaya tıkladığında yeni bir " +
        C(".js") + " dosyasının indiğini görmek.",
    ], title="Bunu Nasıl Doğrularsın?"))

    h.append(quiz(
        ["Lazy loading'i sağlayan şey tam olarak nedir?",
         "Yetkisiz kullanıcıya yönetici kodunu hiç göndermemek için hangi guard?",
         "Preloading lazy loading'in hangi dezavantajını giderir?"],
        ["Dinamik " + C("import()") + " çağrısı. Üstte statik " + C("import") +
         " varsa ayırma gerçekleşmez.",
         C("canMatch") + " — rota eşleşmediği için chunk indirilmez.",
         "Tıklama anındaki kısa bekleme; paketler boşta kalan zamanda önden indirilir."],
    ))
    h.append(takeaways([
        "Lazy loading = kodu ancak gerekince indirmek; kazanç ilk açılıştadır.",
        C("loadComponent") + " tek component, " + C("loadChildren") + " rota grubu içindir.",
        "Ayırmayı <strong>dinamik</strong> " + C("import()") + " sağlar; statik import her şeyi bozar.",
        C("canMatch") + " + lazy = yetkisiz kullanıcı kodu hiç indirmez.",
        C("withPreloading(PreloadAllModules)") + " ile ikisinin de iyi yanını al.",
    ]))

    h.append(lesson_close())
    return "".join(h)


# ---------------------------------------------------------------------------
# 9.6 Nested Routes  (orta derinlik)
# ---------------------------------------------------------------------------
def _lesson_6() -> str:
    h = [lesson_open("9.6", "İç İçe Rotalar — Sabit Kabuk, Değişen İçerik", "m9l6", order=6)]

    h.append(p(
        "Yönetim panellerinin hepsi aynı iskelete sahiptir: solda sabit bir menü, "
        "sağda değişen içerik. Menüyü her sayfaya kopyalamak yerine <strong>iç içe "
        "rotalar</strong> kullanırsın."))

    h.append(h3("Nedir?"))
    h.append(p(
        "<strong>Bir rotanın " + C("children") + " dizisi varsa, o rotanın "
        "component'i bir “kabuk” olur ve çocuk rotalar onun içindeki ikinci bir "
        + C("<router-outlet />") + "'e basılır.</strong>"))

    h.append(h3("Nasıl?"))
    h.append(code('''export const routes: Routes = [
  { path: '', redirectTo: 'panel', pathMatch: 'full' },
  {
    path: 'panel',
    component: Dashboard,                 // KABUK: sidebar + <router-outlet />
    children: [
      { path: '', redirectTo: 'overview', pathMatch: 'full' },
      { path: 'overview', component: Overview },
      { path: 'products', component: ProductList },
      { path: 'products/:id', component: ProductDetail },
    ],
  },
];''', "typescript"))
    h.append(code('''@Component({
  selector: 'app-dashboard',
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <div class="shell">
      <aside class="sidebar">
        <!-- Başında / YOK: göreli yol -> /panel/products -->
        <a routerLink="products" routerLinkActive="active">Ürünler</a>
        <a routerLink="overview" routerLinkActive="active">Genel Bakış</a>
      </aside>

      <section class="main">
        <router-outlet />   <!-- çocuk rota BURAYA -->
      </section>
    </div>
  `,
})
export class Dashboard {}''', "typescript"))
    h.append(tree("""/panel/products      ->  Dashboard  >  ProductList
/panel/products/42   ->  Dashboard  >  ProductDetail
/panel/overview      ->  Dashboard  >  Overview

Dashboard yeniden oluşturulmaz; yalnızca içteki outlet değişir."""))

    h.append(callout("warn", "Başındaki " + C("/") + " her şeyi değiştirir",
                     "<p>" + C('routerLink="products"') + " <strong>göreli</strong>dir: "
                     "bulunduğun rotanın altına gider → " + C("/panel/products") + ".</p>"
                     "<p>" + C('routerLink="/products"') + " ise <strong>mutlak</strong>tır: "
                     "kökten başlar → " + C("/products") + ". Kabuğun içindeyken bunu "
                     "yazarsan ya 404 alırsın ya da paneli terk edersin.</p>"))

    h.append(h3("Göreli gezinme"))
    h.append(table(["Yazım", "Nereye gider"], [
        [C('routerLink="products"'), "Bir alta: " + C("/panel/products")],
        [C('routerLink=".."'), "Bir üste: detaydan listeye"],
        [C('routerLink="../.."'), "İki üste"],
        [C("router.navigate(['..'], { relativeTo: route })"),
         "Koddan göreli gezinme — " + C("relativeTo") + " olmadan mutlak sayılır"],
    ]))

    h.append(callout("note", C("routerLinkActive") + " alt rotalarda da açık kalır",
                     "<p>" + C('routerLink="products"') + " taşıyan menü bağlantısı, "
                     + C("/panel/products/42") + " adresindeyken de <strong>aktif</strong> "
                     "sayılır — çünkü eşleşme varsayılan olarak “bu yolla başlıyor mu?” "
                     "diye bakar. Genelde istediğin budur (mini projede de öyle).</p>"
                     "<p>Yalnızca tam eşleşmede aktif olsun istiyorsan: "
                     + C('[routerLinkActiveOptions]="{ exact: true }"') + ".</p>"))

    h.append(h3("Rota kapsamında servis"))
    h.append(p(
        "Modül 7'de " + C("@Service({ autoProvided: false })") + " ile bir servisi "
        "component kapsamına almıştın. Aynısı rota düzeyinde de yapılabilir: "
        + C("providers") + " yazılan rotada ve tüm çocuklarında <strong>tek bir "
        "örnek</strong> yaşar, o rotadan çıkılınca yok olur."))
    h.append(code('''{
  path: 'panel',
  component: Dashboard,
  providers: [DashboardFilterService],   // yalnızca panel içinde yaşar
  children: [ /* ... */ ],
}''', "typescript"))

    h.append(quiz(
        ["Bir rotayı “kabuk” yapan nedir?",
         C('routerLink="products"') + " ile " + C('routerLink="/products"') + " farkı?",
         "Kabuğun çocuk rotaları neden ikinci bir " + C("<router-outlet />") + " ister?"],
        [C("children") + " dizisi ve component'inde ikinci bir " + C("<router-outlet />") + ".",
         "İlki görelidir (bulunduğun rotanın altına), ikincisi mutlaktır (kökten).",
         "Birinci outlet kabuğu basar; çocuklar kabuğun <strong>içinde</strong> bir "
         "yere basılmalıdır."],
    ))
    h.append(anti([
        "<strong>Çocuk bağlantılarda başa " + C("/") + " koymak.</strong> Göreli "
        "sanırsın, mutlak olur; panelden çıkarsın.",
        "<strong>Kabuk component'inde " + C("<router-outlet />") + " unutmak.</strong> "
        "Menü görünür, içerik hiç gelmez — hata da yoktur.",
        "<strong>Boş çocuk rotada " + C("pathMatch: 'full'") + " yazmamak.</strong> "
        "Yönlendirme her çocuk adresle eşleşir ve döngüye girer.",
    ]))
    h.append(takeaways([
        C("children") + " + ikinci " + C("<router-outlet />") + " = sabit kabuk, değişen içerik.",
        "Kabuk yeniden oluşturulmaz; menü durumu ve kaydırma korunur.",
        "Başında " + C("/") + " olmayan " + C("routerLink") + " görelidir.",
        C("routerLinkActive") + " alt rotalarda da aktiftir; " + C("{ exact: true }") + " ile daraltılır.",
        "Rota düzeyinde " + C("providers") + " ile servis o bölüme kapsanır.",
    ]))

    h.append(lesson_close())
    return "".join(h)


# ---------------------------------------------------------------------------
# Mini proje
# ---------------------------------------------------------------------------
def _mini_proje() -> str:
    h = [lesson_open("—", "Mini Proje: Rol Tabanlı Yönetim Paneli", "m9proje", icon="rocket")]

    h.append(p(
        "Bu modülün altı dersini tek bir uygulamada birleştiriyoruz: sabit "
        "sidebar'lı bir panel, URL'de yaşayan arama ve sayfalama, rota "
        "parametresiyle açılan ürün detayı, role göre kapanan sayfalar ve tembel "
        "yüklenen bir raporlar bölümü."))

    h.append(shot("__SHOT_MAIN__", "Ana ekran: kabuk (sidebar) + ürün listesi. "
                                   "Arama ve sayfa numarası URL'de sorgu parametresi olarak yaşar."))

    h.append(h3("Rota haritası"))
    h.append(code("""'' ................ -> redirect 'panel'
'panel' ........... -> Dashboard  (KABUK: sidebar + <router-outlet />)
   '' ............. -> redirect 'genel-bakis'  (pathMatch: 'full')
   'genel-bakis' .. -> Overview
   'urunler' ...... -> ProductList     (sorgu param: q, page, pageSize)
   'urunler/:id' .. -> ProductDetail   (yol param + resolver)
   'yeni-urun' .... -> ProductCreate   (canActivate: adminGuard,
                                        canDeactivate: unsavedChangesGuard)
   'raporlar' ..... -> LAZY loadComponent + canMatch: adminGuard
'yetkisiz' ........ -> Denied
'**' .............. -> NotFound""", "typescript"))

    h.append(shot("__SHOT_DETAIL__", "Ürün detayı: id yol parametresinden gelir, "
                                     "ürün resolver ile hazır gelir — yükleniyor ekranı yok."))

    h.append(h3("Özellikler / Gereksinimler"))
    h.append("""<ul>
<li><strong>Kabuk:</strong> sol menü ve üst şerit sabit kalsın; yalnızca sağdaki
alan değişsin (iç içe rotalar).</li>
<li><strong>Liste:</strong> ürünler API'den sayfalı gelsin. Arama terimi, sayfa ve
sayfa boyutu <strong>URL'de sorgu parametresi</strong> olarak dursun — adresi
kopyalayıp yeni sekmede açınca aynı ekran gelmeli.</li>
<li><strong>Detay:</strong> “Detay” bağlantısı <code class="inline">/panel/urunler/:id</code>
adresine gitsin; ürün <strong>resolver</strong> ile hazır gelsin. Ürün yoksa
sayfa hiç açılmasın, listeye yönlensin.</li>
<li><strong>Rol:</strong> üst şeritteki seçici rolü <code class="inline">'admin'</code> /
<code class="inline">'viewer'</code> arasında değiştirsin (bir servisteki signal).</li>
<li><strong>Yeni Ürün:</strong> yalnızca admin girebilsin
(<code class="inline">canActivate</code>). Viewer denerse <code class="inline">/yetkisiz</code>
ekranına yönlensin.</li>
<li><strong>Kaydedilmemiş değişiklik:</strong> form doluyken sayfadan çıkılmak
istenirse onay sorulsun (<code class="inline">canDeactivate</code>).</li>
<li><strong>Raporlar:</strong> tembel yüklensin ve <code class="inline">canMatch</code>
ile korunsun — viewer rolündeyken chunk hiç inmemeli (Network sekmesinden doğrula).</li>
<li><strong>404:</strong> tanımsız adresler için bir sayfa olsun.</li>
<li><strong>Biçimlendirme:</strong> fiyat <code class="inline">currency</code> pipe ile,
stok rozeti kendi directive'inle renklensin (Modül 6).</li>
</ul>""")

    h.append(shot("__SHOT_DENIED__", "Viewer rolündeyken yönetici sayfası denendiğinde: "
                                     "guard düz false değil, yönlendirme döndürür."))

    h.append(h3("Angular tarafı (sende) — ipuçları"))
    h.append("""<ul>
<li><strong>Başlangıç:</strong> <code class="inline">provideRouter(routes,
withComponentInputBinding())</code> — bunu ilk iş olarak ekle, yoksa parametreler
sessizce <code class="inline">undefined</code> gelir.</li>
<li><strong>Rol servisi:</strong> <code class="inline">@Service()</code> içinde
<code class="inline">private readonly _role = signal&lt;'admin' | 'viewer'&gt;('admin')</code>,
dışarı <code class="inline">asReadonly()</code> + bir <code class="inline">setRole()</code>
metodu (Modül 7 kalıbı).</li>
<li><strong>Liste:</strong> <code class="inline">q</code>, <code class="inline">page</code>,
<code class="inline">pageSize</code> birer <code class="inline">input()</code> olsun;
<code class="inline">httpResource</code> bunları okuyunca URL değişince veri
kendiliğinden tazelenir. Sayısal olanlarda
<code class="inline">transform: numberAttribute</code> unutma.</li>
<li><strong>Arama kutusu:</strong> değeri doğrudan servise yazmak yerine
<code class="inline">router.navigate([], { queryParams: { q, page: 1 },
queryParamsHandling: 'merge' })</code> ile URL'e yaz — tek doğruluk kaynağı URL olsun.</li>
<li><strong>Sayfalama:</strong> aynı mantık; <code class="inline">page</code>'i
<code class="inline">merge</code> ile güncelle, arama kaybolmasın.</li>
<li><strong>Detay bağlantısı:</strong> kabuk içindesin — göreli yaz:
<code class="inline">[routerLink]="[product.id]"</code>.</li>
<li><strong>Resolver:</strong> <code class="inline">ResolveFn&lt;Product |
RedirectCommand&gt;</code>; hata durumunda
<code class="inline">new RedirectCommand(router.parseUrl('/panel/urunler'))</code>.</li>
<li><strong>Guard'lar:</strong> <code class="inline">inject()</code> çağrılarını
fonksiyonun en üstünde yap. <code class="inline">adminGuard</code> hem
<code class="inline">canActivate</code> hem <code class="inline">canMatch</code>
olarak kullanılabilir — ikisinde de aynı fonksiyon.</li>
<li><strong>Kilitli menü:</strong> viewer rolünde menüdeki yönetici bağlantılarına
<code class="inline">[class.locked]="!isAdmin()"</code> ver — guard'ı UI'da da göster.</li>
<li><strong>Lazy:</strong> raporlar için <strong>yalnızca</strong> dinamik
<code class="inline">import()</code>; dosyanın üstüne o component'i import etme.</li>
</ul>""")

    h.append(recall([
        "Modül 5: " + C("signal") + " / " + C("computed") + ", immutable güncelleme.",
        "Modül 6: " + C("currency") + " pipe ve stok rozeti için custom directive "
        "(" + C("host") + " + selector adıyla aynı input).",
        "Modül 7: " + C("@Service()") + " + " + C("inject()") + ", servisin dışarı "
        "sade bir yüzey vermesi.",
        "Modül 8: " + C("httpResource") + ", " + C("HttpClient") + " ile yazma, "
        "interceptor'lar, " + C("?delay=1500") + " ile yükleniyor ekranını denemek.",
        "Modül 9: rotalar, parametreler, guard'lar, resolver, lazy loading, iç içe rotalar.",
    ], title="Bu Projede Birleşen Modüller"))

    h.append(callout("info", "Materyaller ve API",
                     "<p>Statik referansı ayrıca verdim (JS yok): " + C("index.html") +
                     ", " + C("detail.html") + ", " + C("denied.html") + ", "
                     + C("styles.scss") + ", " + C("styles.css") + " ve üç ekran "
                     "görüntüsü. HTML'lerin başındaki yorum blokları rota haritasını "
                     "ve her parçanın Angular karşılığını anlatıyor.</p>"
                     "<p>API olarak Modül 8'deki " + C("Module08ProductApi") + "'yi "
                     "kullan: " + C("/api/products") + " (sorgu parametreleri: "
                     + C("name") + ", " + C("page") + ", " + C("pageSize") + ", "
                     + C("sort") + ") ve " + C("/api/products/{id}") + ". Resolver'ın "
                     "yönlendirme dalını denemek için var olmayan bir id ile "
                     + C("/panel/urunler/999999") + " adresini aç.</p>"))

    h.append(takeaways([
        "Ekran durumunun bir kısmı URL'e taşındı: adres artık paylaşılabilir.",
        "Kabuk + çocuk rota deseni: menü bir kez yazılır, içerik değişir.",
        "Guard'lar arayüzü düzenler; " + C("canMatch") + " ayrıca kod indirmeyi de engeller.",
        "Resolver, detay sayfasındaki yükleniyor/boş durum kodunu tamamen kaldırdı.",
        "Önceki beş modülün araçları (signal, pipe, directive, servis, HTTP) "
        "burada tek bir uygulamada buluştu.",
    ]))

    h.append(lesson_close())
    return "".join(h)


# ---------------------------------------------------------------------------
# Özet
# ---------------------------------------------------------------------------
def _summary() -> str:
    h = [lesson_open("—", f"Modül {MODULE_NO} Özeti", "m9ozet", icon="flag")]

    h.append(p(
        "Uygulaman artık tek ekranlı değil: adresi olan, geri tuşu çalışan, linki "
        "paylaşılabilen bir uygulama."))
    h.append("""<ul>
<li><strong>Kurulum:</strong> <code class="inline">routes</code> +
<code class="inline">provideRouter(routes, withComponentInputBinding())</code> +
<code class="inline">&lt;router-outlet /&gt;</code>.</li>
<li><strong>Gezinme:</strong> şablondan <code class="inline">routerLink</code>,
koddan <code class="inline">router.navigate([...])</code>.</li>
<li><strong>Parametreler:</strong> aynı adlı <code class="inline">input()</code> ile
bağlanır; değerler string gelir, sayı için
<code class="inline">numberAttribute</code>.</li>
<li><strong>Guard'lar:</strong> <code class="inline">canActivate</code> /
<code class="inline">canMatch</code> / <code class="inline">canDeactivate</code> —
<code class="inline">false</code> yerine <code class="inline">UrlTree</code>.</li>
<li><strong>Resolver:</strong> veri hazır gelsin, component sadeleşsin;
her yerde değil.</li>
<li><strong>Lazy:</strong> dinamik <code class="inline">import()</code>;
<code class="inline">canMatch</code> ile birleşince chunk hiç inmez.</li>
<li><strong>İç içe rotalar:</strong> <code class="inline">children</code> + ikinci
outlet = sabit kabuk.</li>
</ul>""")

    h.append(callout("info", "Sırada ne var?",
                     "<p><strong>Modül 10 — Project Structure &amp; Feature-Based "
                     "Architecture:</strong> Dokuz modüldür dosyaları biraz da "
                     "sezgiyle yerleştiriyoruz. Sırada bunun kuralları var: "
                     + C("core") + " / " + C("shared") + " / " + C("features") +
                     " ayrımı, bağımlılık yönü kuralları, barrel export'lar, "
                     + C("tsconfig.json") + " yol takma adları ve mimariyi ESLint "
                     "ile korumak. Bu modülde kurduğun rota haritası, oradaki "
                     "klasör yapısının iskeleti olacak.</p>"))

    h.append(p(
        "<strong>Takıldığın her yeri sor</strong> — mini projeyi yapıp "
        "gösterdiğinde birlikte gözden geçiririz. Kolay gelsin!"))

    h.append(lesson_close())
    return "".join(h)


def render() -> str:
    return (_divider() + _lesson_1() + _lesson_2() + _lesson_3() + _lesson_4()
            + _lesson_5() + _lesson_6() + _mini_proje() + _summary())
