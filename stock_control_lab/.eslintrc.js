{
  "env": {
    "browser": true,
    "es2021": true,
    "node": true
  },
  "extends": [
    "eslint:recommended",
    "plugin:vue/vue3-essential",
    "plugin:import/errors",
    "plugin:import/warnings"
  ],
  "parserOptions": {
    "ecmaVersion": 12,
    "sourceType": "module"
  },
  "plugins": [
    "vue",
    "import"
  ],
  "rules": {
    "indent": ["error", 2],
    "linebreak-style": ["error", "unix"],
    "quotes": ["error", "single"],
    "semi": ["error", "always"],
    "no-unused-vars": "warn",
    "no-console": "off",
    "import/order": [
      "error",
      {
        "groups": ["builtin", "external", "internal"],
        "pathGroups": [
          {
            "pattern": "vue",
            "group": "external",
            "position": "before"
          }
        ],
        "pathGroupsExcludedImportTypes": ["vue"],
        "alphabetize": {
          "order": "asc",
          "caseInsensitive": true
        }
      }
    ],
    "vue/html-indent": ["error", 2],
    "vue/max-attributes-per-line": [
      "error",
      {
        "singleline": {
          "max": 3
        },
        "multiline": {
          "max": 1
        }
      }
    ],
    "vue/html-self-closing": [
      "error",
      {
        "html": {
          "void": "always",
          "normal": "never",
          "component": "always"
        },
        "svg": "always",
        "math": "always"
      }
    ],
    "vue/component-name-in-template-casing": [
      "error",
      "PascalCase"
    ]
  },
  "globals": {
    "defineProps": "readonly",
    "defineEmits": "readonly",
    "defineExpose": "readonly",
    "withDefaults": "readonly",
    "Alpine": "readonly",
    "htmx": "readonly",
    "Chart": "readonly",
    "axios": "readonly"
  },
  "settings": {
    "import/resolver": {
      "node": {
        "extensions": [".js", ".jsx", ".ts", ".tsx", ".vue"]
      }
    }
  },
  "overrides": [
    {
      "files": ["*.vue"],
      "rules": {
        "vue/script-indent": ["error", 2, { "baseIndent": 1 }]
      }
    },
    {
      "files": ["*.js"],
      "rules": {
        "indent": ["error", 2]
      }
    }
  ]
}