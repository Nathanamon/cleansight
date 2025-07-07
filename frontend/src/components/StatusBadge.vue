<template>
  <span :class="badgeClasses">
    <i :class="iconClass" v-if="showIcon"></i>
    {{ statusText }}
  </span>
</template>

<script>
export default {
  name: 'StatusBadge',
  props: {
    status: {
      type: String,
      required: true,
      validator: (value) => ['pleine', 'vide', 'vidée', 'maintenance', 'erreur'].includes(value)
    },
    showIcon: {
      type: Boolean,
      default: false
    },
    size: {
      type: String,
      default: 'sm',
      validator: (value) => ['xs', 'sm', 'md', 'lg'].includes(value)
    }
  },
  computed: {
    statusConfig() {
      const configs = {
        pleine: {
          text: 'Pleine',
          classes: 'bg-red-100 text-red-800 border-red-200',
          icon: 'fas fa-exclamation-circle'
        },
        vide: {
          text: 'Vide',
          classes: 'bg-green-100 text-green-800 border-green-200',
          icon: 'fas fa-check-circle'
        },
        vidée: {
          text: 'Vidée',
          classes: 'bg-green-100 text-green-800 border-green-200',
          icon: 'fas fa-check-circle'
        },
        maintenance: {
          text: 'Maintenance',
          classes: 'bg-yellow-100 text-yellow-800 border-yellow-200',
          icon: 'fas fa-tools'
        },
        erreur: {
          text: 'Erreur',
          classes: 'bg-gray-100 text-gray-800 border-gray-200',
          icon: 'fas fa-times-circle'
        }
      };
      return configs[this.status] || configs.erreur;
    },
    badgeClasses() {
      const sizeClasses = {
        xs: 'px-2 py-1 text-xs',
        sm: 'px-3 py-1 text-sm',
        md: 'px-4 py-2 text-base',
        lg: 'px-6 py-3 text-lg'
      };
      
      return [
        'inline-flex items-center rounded-full font-medium border',
        this.statusConfig.classes,
        sizeClasses[this.size]
      ].join(' ');
    },
    statusText() {
      return this.statusConfig.text;
    },
    iconClass() {
      return `${this.statusConfig.icon} mr-1`;
    }
  }
}
</script>