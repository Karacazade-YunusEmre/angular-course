# -*- coding: utf-8 -*-
"""Tam müfredat (30 modül) ve modül dosya adları.

Yeni bir modül tamamlandığında: FUTURE'dan çıkar, DONE_FILES'a ekle.
build_toc.py bu dosyayı okuyarak içindekiler tablosunu üretir.
"""

# PDF dosya adlarındaki slug: Modul-09-Routing.pdf
MODULE_SLUGS = {
    1: "Temeller", 2: "TypeScript", 3: "CLI-DevTools", 4: "Components",
    5: "Signals", 6: "Directives-Pipes", 7: "Services-DI", 8: "HTTP",
    9: "Routing", 10: "Project-Structure", 11: "RxJS", 12: "State-Management",
    13: "Material-CDK", 14: "Forms", 15: "Animations", 16: "Lazy-Loading",
    17: "WebSockets", 18: "i18n", 19: "Accessibility", 20: "Security",
    21: "Testing", 22: "Performance", 23: "Error-Handling", 24: "Environment-Config",
    25: "SSR", 26: "PWA", 27: "Microfrontend", 28: "Design-Patterns",
    29: "CI-CD", 30: "Capstone",
}

# Seviye grupları (içindekiler tablosunda başlık olarak görünür)
LEVELS = [
    ("Başlangıç · Sıfır → Junior", [1, 2, 3, 4]),
    ("Gelişim · Junior → Mid-Level", [5, 6, 7, 8, 9, 10, 11, 12, 13]),
    ("Olgunlaşma · Mid → Senior", [14, 15, 16, 17, 18, 19, 20, 21]),
    ("Profesyonel · Senior", [22, 23, 24, 25, 26]),
    ("Expert · Senior → Expert", [27, 28, 29]),
    ("Capstone · Final Proje", [30]),
]

# Tamamlanan modüller. Başlık ve ders listesi PDF'in kendi yer imlerinden
# okunur; burada yalnızca dosya adı tutulur.
DONE_FILES = {
    1: "Modul-01-Temeller.pdf",
    2: "Modul-02-TypeScript.pdf",
    3: "Modul-03-CLI-DevTools.pdf",
    4: "Modul-04-Components.pdf",
    5: "Modul-05-Signals.pdf",
    6: "Modul-06-Directives-Pipes.pdf",
    7: "Modul-07-Services-DI.pdf",
    8: "Modul-08-HTTP.pdf",
}

# Henüz işlenmemiş modüller: (başlık, planlanan ders başlıkları)
FUTURE = {
    9: ("Routing & Navigation", [
        "Temel routing", "Route parameters & component input binding",
        "Functional guards", "Functional resolvers", "Lazy loading routes",
        "Nested routes", "Mini proje: Multi-role dashboard"]),
    10: ("Project Structure & Feature-Based Architecture", [
        "Neden klasör yapısı önemli?", "Feature-based architecture",
        "core / shared / features ayrımı", "Bağımlılık kuralları",
        "Index files (barrel exports)", "Path aliases (tsconfig.json)",
        "ESLint rules ile mimariyi korumak", "Mini proje: Project skeleton"]),
    11: ("RxJS Deep-Dive", [
        "Observable: stream over time", "Operators: 4 kategori",
        "Higher-order mapping operators", "Subjects",
        "Hot vs cold observables", "Error handling", "Memory leak prevention",
        "RxJS + signals interop", "Mini proje: Smart search"]),
    12: ("State Management (NgRx Signal Store)", [
        "Hangi araç ne zaman?", "Service + signal ile basit state",
        "NgRx Signal Store setup", "Signal Store anatomisi", "Component'ta kullanım",
        "withEntities", "Feature store", "Mini proje: Shopping cart"]),
    13: ("Angular Material & CDK", [
        "Neden UI library?", "UI library karşılaştırması", "Angular Material setup",
        "Theming (Material Design 3)", "Sık kullanılan component'lar", "MatDialog",
        "Angular CDK nedir?", "CDK drag & drop", "CDK overlay", "CDK virtual scrolling",
        "CDK layout", "Mini proje: Material admin dashboard"]),
    14: ("Forms (Reactive + Signal Forms)", [
        "Forms yaklaşımları", "Reactive Forms temelleri", "Typed forms",
        "FormArray", "Custom validators", "Cross-field validation",
        "Conditional validation", "Signal Forms (v22)", "Mini proje: Multi-step wizard"]),
    15: ("Animations", [
        "Setup", "Trigger, state, transition", ":enter & :leave", "Stagger",
        "Route animations", "Reduced motion desteği", "Mini proje: Animated card gallery"]),
    16: ("Lazy Loading & @defer", [
        "3 seviyeli lazy loading", "@defer tetikleyicileri", "Tam @defer sözdizimi",
        "Prefetch stratejileri", "NgOptimizedImage", "Mini proje: E-commerce product page"]),
    17: ("WebSockets & Real-Time Communication", [
        "Real-time: 3 yaklaşım", "RxJS WebSocket subject", "Reconnection strategy",
        "Server-sent events (SSE)", "Socket.IO entegrasyonu", "Mini proje: Real-time chat"]),
    18: ("i18n (Internationalization)", [
        "Yaklaşımlar", "Transloco (önerilen)", "Locale-aware pipes", "RTL support",
        "Pluralization & ICU messages", "Mini proje: Multi-language blog"]),
    19: ("Accessibility (a11y) & Angular Aria", [
        "Neden a11y?", "WCAG 2.2 (POUR)", "Semantic HTML first", "ARIA attributes",
        "Angular Aria", "Focus management", "Klavye navigasyonu",
        "Testing", "Mini proje: Accessible form & modal"]),
    20: ("Security", [
        "Web security temelleri (OWASP)", "XSS koruması", "DomSanitizer",
        "Content security policy", "CSRF protection", "JWT storage stratejileri",
        "Dependency security", "Sensitive data handling", "Mini proje: Secure auth flow"]),
    21: ("Testing (Vitest + Playwright)", [
        "Test pyramidi", "Vitest setup", "Component testing", "Service mocking",
        "Signal testing", "Signal Store testing", "E2E with Playwright",
        "Mini proje: %80+ coverage"]),
    22: ("Performance & Change Detection", [
        "Change detection: zone vs zoneless", "OnPush vs Eager", "Memory leaks",
        "Bundle size optimization", "Track-by optimization", "Performance profiling",
        "Web vitals", "Mini proje: Performance audit"]),
    23: ("Error Handling & Logging", [
        "Neden önemli?", "Global ErrorHandler", "HTTP error interceptor",
        "User-friendly error UI", "Sentry entegrasyonu", "Logging service pattern",
        "Performance monitoring", "Mini proje: Error-resilient app"]),
    24: ("Environment Config & Build Configurations", [
        "Environment files", "angular.json build configurations", "Runtime configuration",
        "Feature flags", "Build optimization", "Source maps stratejisi",
        "Mini proje: Multi-environment setup"]),
    25: ("SSR, Hydration & Web Vitals", [
        "Neden SSR?", "Setup", "Hydration", "Incremental hydration",
        "Server-only / client-only code", "SEO meta tags", "Mini proje: SEO-optimized blog"]),
    26: ("PWA (Progressive Web Apps)", [
        "PWA nedir?", "Setup", "Service worker caching", "Update notifications",
        "Push notifications", "Install prompt", "Offline detection",
        "Mini proje: Offline-first notes app"]),
    27: ("Microfrontend Architecture", [
        "Microfrontend nedir?", "Module Federation", "Native Federation",
        "Inter-MFE communication", "@defer + Module Federation",
        "Mini proje: E-commerce microfrontend"]),
    28: ("Design Patterns", [
        "Smart vs dumb components", "Repository pattern", "Facade pattern",
        "Strategy pattern", "Observer pattern (built-in)", "Mini proje: Architecture refactor"]),
    29: ("CI/CD & Deployment", [
        "Build pipeline anatomisi", "GitHub Actions", "Docker",
        "Vercel / Netlify deployment", "Cloudflare Pages", "Self-hosting (Nginx + VPS)",
        "SSR deployment stratejileri", "Environment variables in CI",
        "Mini proje: Full CI/CD pipeline"]),
    30: ("Capstone — Task Management Platform", [
        "H1 Mimari tasarım + skeleton", "H2 Shell + auth + routing + Material",
        "H3 MFE-Projects (CRUD, formlar)", "H4 MFE-Tasks (@defer, drag-drop, real-time)",
        "H5 MFE-Reports (dashboard, virtual scroll)", "H6 State management (Signal Store)",
        "H7 i18n + a11y + security audit", "H8 Testing + error handling + monitoring",
        "H9 SSR + PWA", "H10 CI/CD + production deployment"]),
}
