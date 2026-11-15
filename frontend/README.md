# Interface Scenora (prévue)

L'interface sera développée en **React + TypeScript + Vite**, avec **Tailwind CSS** et **React Konva** pour le plan 2D.
Elle n'est pas encore dans le dépôt : la première soumission (15 novembre) porte sur le backend et le moteur de continuité.

Organisation prévue :

```text
frontend/src/
├── components/
├── pages/
├── features/
│   ├── projects/
│   ├── screenplay/
│   ├── scenes/
│   ├── shotlist/
│   ├── storyboard/
│   ├── spatial/
│   └── continuity/
├── services/   appels à l'API FastAPI
└── types/      types générés à partir des schémas Pydantic
```

Identité visuelle : anthracite #222321, ivoire chaud #F1EBDD, bordeaux #873E43, or mat #B58C5A ; polices Playfair Display et Inter.
