<template>
  <!-- Fond dégradé doux et carte centrale en verre dépoli pour une esthétique plus "premium" -->
  <div class="min-h-screen bg-gradient-to-b from-emerald-50 via-white to-white py-16 px-4 sm:px-6">
    <article class="prose lg:prose-lg mx-auto max-w-3xl bg-white/80 backdrop-blur-sm shadow-2xl rounded-3xl px-8 sm:px-12 py-14 text-gray-800">
      <header class="text-center mb-8">
        <h1 class="mb-2">Politique de confidentialité – CleanSight</h1>
        <p class="text-sm italic text-gray-500">
          Dernière mise à jour&nbsp;: <time datetime="2025-07-01">1 juillet 2025</time>
        </p>
      </header>

      <section aria-labelledby="collecte" class="scroll-mt-24">
        <h2 id="collecte">1. Données que nous collectons</h2>
        <p>Lorsque vous utilisez CleanSight, nous enregistrons&nbsp;:</p>
        <ul>
          <li>les images de poubelles que vous téléchargez&nbsp;;</li>
          <li>les annotations que vous validez (pleine ou vide)&nbsp;;</li>
          <li>les métadonnées associées — date, dimensions, taille de fichier, modèle d’appareil photo et position GPS si elle est fournie.</li>
        </ul>
      </section>

      <section aria-labelledby="utilisation" class="mt-10 scroll-mt-24">
        <h2 id="utilisation">2. Pourquoi nous les utilisons</h2>
        <p>Ces informations nous permettent&nbsp;:</p>
        <ul>
          <li>d’entraîner et d’évaluer nos algorithmes de classification des déchets&nbsp;;</li>
          <li>de vous proposer des recommandations optimisées de collecte pour votre territoire&nbsp;;</li>
          <li>de produire des statistiques agrégées et anonymisées sur les taux de remplissage des conteneurs.</li>
        </ul>
      </section>

      <section aria-labelledby="partage" class="mt-10 scroll-mt-24">
        <h2 id="partage">3. Partage avec des tiers</h2>
        <p>Nous ne transmettons jamais vos images ni vos annotations à des tiers sans votre consentement explicite, sauf si la loi l’exige ou pour défendre nos droits en justice.</p>
      </section>

      <section aria-labelledby="securite" class="mt-10 scroll-mt-24">
        <h2 id="securite">4. Sécurité et lieu de stockage</h2>
        <p>Vos données sont hébergées dans l’Espace économique européen sur des serveurs certifiés ISO&nbsp;27001. Elles sont chiffrées au repos (<abbr title="Advanced Encryption Standard">AES‑256</abbr>) et lors de leur transport (<abbr title="Transport Layer Security">TLS&nbsp;1.3</abbr>).</p>
      </section>

      <section aria-labelledby="conservation" class="mt-10 scroll-mt-24">
        <h2 id="conservation">5. Durée de conservation</h2>
        <p>Les images et annotations sont conservées pendant <strong>deux&nbsp;ans</strong> à compter de leur collecte. Elles sont ensuite soit anonymisées, soit définitivement supprimées, conformément aux réglementations en vigueur.</p>
      </section>

      <section aria-labelledby="droits" class="mt-10 scroll-mt-24">
        <h2 id="droits">6. Vos droits</h2>
        <p>Conformément au <abbr title="Règlement Général sur la Protection des Données">RGPD</abbr>, vous pouvez&nbsp;:</p>
        <ul>
          <li>demander l’accès à vos données personnelles&nbsp;;</li>
          <li>en obtenir la rectification ou la suppression&nbsp;;</li>
          <li>vous opposer ou demander la limitation de certains traitements&nbsp;;</li>
          <li>retirer votre consentement à tout moment lorsque le traitement repose sur celui‑ci.</li>
        </ul>
        <p>
          Pour exercer ces droits, contactez notre délégué à la protection des données (DPO) à l’adresse&nbsp;:
          <br />
          <a href="mailto:privacy@cleansight.local" class="font-semibold underline-offset-4 hover:text-green-700 dark:hover:text-green-500">privacy@cleansight.local</a>
        </p>
      </section>

      <section aria-labelledby="modifications" class="mt-10 scroll-mt-24">
        <h2 id="modifications">7. Modifications de cette politique</h2>
        <p>Nous pouvons être amenés à mettre à jour cette politique pour refléter les évolutions légales ou fonctionnelles du service. En cas de changement substantiel, nous vous en informerons au moins quinze&nbsp;jours à l’avance via l’application et/ou par e‑mail.</p>
      </section>

      <section aria-labelledby="contact" class="mt-10 scroll-mt-24">
        <h2 id="contact">8. Nous contacter</h2>
        <p>Pour toute question relative à cette politique ou à vos données personnelles&nbsp;:</p>
        <p class="not-prose">
          <a href="mailto:privacy@cleansight.local" class="inline-flex items-center gap-2 rounded-full bg-green-600 text-white px-4 py-2 text-sm font-medium shadow-lg hover:bg-green-700 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0l-9.75 6.5-9.75-6.5m19.5 0L12 13.25m0 0L2.25 6.75" />
            </svg>
            privacy@cleansight.local
          </a>
        </p>
        <address class="mt-4 not-italic leading-relaxed">
          CleanSight – Service Protection des données<br />
          10&nbsp;rue de l’Environnement<br />
          75012&nbsp;Paris, France
        </address>
      </section>
    </article>
  </div>
</template>

<script setup lang="ts">
// Aucun script requis pour le moment
</script>

<style lang="postcss">
@layer base {
  :root {
    /* Couleur des liens dans les blocs prose */
    --tw-prose-links: theme(colors.green.600);
  }
}

/* Hide the default marker on headings appearing in the prose plugin */
.prose :where(h2):not(:where([class~="not-prose"] *))::after {
  display: none;
}

/* Ajoute une transition douce aux liens */
a {
  @apply transition-colors duration-200;
}
</style>