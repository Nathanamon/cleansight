<template>
  <!-- Mise en forme premium identique à la politique de confidentialité -->
  <div class="min-h-screen bg-gradient-to-b from-emerald-50 via-white to-white py-16 px-4 sm:px-6">
    <article class="prose lg:prose-lg mx-auto max-w-3xl bg-white/80 backdrop-blur-sm shadow-2xl rounded-3xl px-8 sm:px-12 py-14 text-gray-800">
      <header class="text-center mb-8">
        <h1 class="mb-2">Conditions d’utilisation – CleanSight</h1>
        <p class="text-sm italic text-gray-500">
          Dernière mise à jour&nbsp;: <time datetime="2025-07-01">1 juillet 2025</time>
        </p>
      </header>

      <section aria-labelledby="objet" class="scroll-mt-24">
        <h2 id="objet">1. Objet</h2>
        <p>Les présentes Conditions d’utilisation (ci-après « les&nbsp;Conditions ») régissent l’accès et l’utilisation de la plateforme CleanSight, un service d’analyse automatique d’images de poubelles destiné à optimiser la collecte des déchets.</p>
      </section>

      <section aria-labelledby="acces" class="mt-10 scroll-mt-24">
        <h2 id="acces">2. Accès au service</h2>
        <ul>
          <li>L’accès à CleanSight est réservé aux collectivités et partenaires expressément autorisés.</li>
          <li>L’utilisateur garantit détenir l’intégralité des droits sur les images qu’il transmet et s’engage à ne pas télécharger de contenu illicite, diffamatoire ou portant atteinte à la vie privée.</li>
        </ul>
      </section>

      <section aria-labelledby="responsabilites" class="mt-10 scroll-mt-24">
        <h2 id="responsabilites">3. Responsabilités</h2>
        <p>CleanSight fournit une prédiction « pleine » ou « vide » basée sur des règles et modèles d’intelligence artificielle. Cette prédiction constitue une aide à la décision : la responsabilité finale concernant la collecte ou non des déchets incombe exclusivement à l’utilisateur.</p>
      </section>

      <section aria-labelledby="propriete" class="mt-10 scroll-mt-24">
        <h2 id="propriete">4. Propriété intellectuelle</h2>
        <p>Tous les droits de propriété intellectuelle relatifs à CleanSight (code source, modèles, règles d’IA, documentation et éléments graphiques) sont la propriété exclusive de l’équipe CleanSight ou de ses concédants. Toute reproduction ou utilisation non autorisée est interdite.</p>
      </section>

      <section aria-labelledby="modif" class="mt-10 scroll-mt-24">
        <h2 id="modif">5. Modification des Conditions</h2>
        <p>Nous nous réservons le droit de modifier les présentes Conditions à tout moment. Les modifications seront publiées sur cette page accompagnées de la date de mise à jour et entreront en vigueur quinze&nbsp;jours après leur publication, sauf mention contraire.</p>
      </section>

      <section aria-labelledby="contact" class="mt-10 scroll-mt-24">
        <h2 id="contact">6. Contact</h2>
        <p>Pour toute question relative à ces Conditions ou au service, vous pouvez nous écrire&nbsp;:</p>
        <p class="not-prose">
          <a href="mailto:contact@cleansight.local" class="inline-flex items-center gap-2 rounded-full bg-green-600 text-white px-4 py-2 text-sm font-medium shadow-lg hover:bg-green-700 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0l-9.75 6.5-9.75-6.5m19.5 0L12 13.25m0 0L2.25 6.75" />
            </svg>
            contact@cleansight.local
          </a>
        </p>
        <address class="mt-4 not-italic leading-relaxed">
          CleanSight – Service juridique<br />
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
    --tw-prose-links: theme(colors.green.600);
  }
}

/* Cohérence visuelle : mêmes ajustements que la politique de confidentialité */
.prose :where(h2):not(:where([class~="not-prose"] *))::after {
  display: none;
}

a {
  @apply transition-colors duration-200;
}
</style>