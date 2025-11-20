# DataPurity Frontend

React + TypeScript frontend for the DataPurity SaaS platform.

## Quick Start

1. **Install dependencies:**

```powershell
npm install
```

2. **Set up environment variables:**

```powershell
cp ..\infra\env\frontend.env.example .env
# Edit .env with your configuration
```

3. **Start dev server:**

```powershell
npm run dev
```

Visit http://localhost:3000

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Project Structure

- `src/components/` - Reusable React components
- `src/pages/` - Page components
- `src/layouts/` - Layout components
- `src/hooks/` - Custom React hooks
- `src/types/` - TypeScript type definitions
- `src/config/` - Configuration files
- `src/pwa/` - PWA setup
- `src/styles/` - CSS files

## Building for Production

```powershell
npm run build
```

Output will be in the `dist/` directory.

## PWA

This app is configured as a Progressive Web App. It can be installed on desktop and mobile devices and supports offline mode.
