---
name: Executive Intelligence
colors:
  surface: '#f7f9fb'
  surface-dim: '#d8dadc'
  surface-bright: '#f7f9fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f4f6'
  surface-container: '#eceef0'
  surface-container-high: '#e6e8ea'
  surface-container-highest: '#e0e3e5'
  on-surface: '#191c1e'
  on-surface-variant: '#45464d'
  inverse-surface: '#2d3133'
  inverse-on-surface: '#eff1f3'
  outline: '#76777d'
  outline-variant: '#c6c6cd'
  surface-tint: '#565e74'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#131b2e'
  on-primary-container: '#7c839b'
  inverse-primary: '#bec6e0'
  secondary: '#006c49'
  on-secondary: '#ffffff'
  secondary-container: '#6cf8bb'
  on-secondary-container: '#00714d'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#0b1c30'
  on-tertiary-container: '#75859d'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae2fd'
  primary-fixed-dim: '#bec6e0'
  on-primary-fixed: '#131b2e'
  on-primary-fixed-variant: '#3f465c'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#d3e4fe'
  tertiary-fixed-dim: '#b7c8e1'
  on-tertiary-fixed: '#0b1c30'
  on-tertiary-fixed-variant: '#38485d'
  background: '#f7f9fb'
  on-background: '#191c1e'
  surface-variant: '#e0e3e5'
typography:
  headline-lg:
    fontFamily: Geist
    fontSize: 40px
    fontWeight: '600'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Geist
    fontSize: 30px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Geist
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
    letterSpacing: '0'
  body-md:
    fontFamily: Geist
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: '0'
  label-md:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  container-max: 1280px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 48px
---

## Brand & Style

This design system is built for a high-end financial AI context, prioritizing clarity, precision, and trust. The aesthetic sits at the intersection of **Corporate Modern** and **Minimalism**, utilizing significant whitespace to reduce cognitive load during complex financial decision-making. 

The emotional response should be one of "calm authority." The UI does not compete for attention; instead, it provides a structured canvas for data and AI-driven insights. Design elements are refined through subtle glassmorphism for secondary overlays and a rigorous adherence to a systematic grid.

## Colors

The palette is anchored by **Deep Slate (#0F172A)**, used for primary actions, navigation, and user-initiated message bubbles to convey stability and "Executive" status. **Emerald Green (#10B981)** is used sparingly as a high-signal accent for growth, positive trends, and AI "active" states.

Backgrounds utilize a tiered grayscale to create structural depth without heavy lines:
- **Base:** #FFFFFF (Primary workspace)
- **Surface:** #F8FAFC (Card backgrounds and subtle sections)
- **Muted:** #F1F5F9 (Dividers and disabled states)

## Typography

The design system utilizes **Geist** for its technical precision and monospaced-influenced tracking, which excels in data-heavy fintech environments. 

**Hierarchy Rules:**
- **Headlines:** Use tight letter-spacing (-0.02em) to maintain a premium, "locked-in" look.
- **Body:** Standard tracking for maximum readability in long AI responses.
- **Labels:** Uppercase treatment is permitted for `label-sm` when used in table headers or small metadata tags to increase scannability.

## Layout & Spacing

The layout follows a **Fixed Grid** model for desktop to maintain the "Executive Dashboard" feel, centering content at a maximum width of 1280px. 

**Rhythm:**
- Use a 4px baseline shift for all minor adjustments.
- Component padding should default to 24px (6 units) for standard cards.
- **Mobile:** Transition to a fluid single-column layout with 16px side margins.
- **AI Chat Interface:** The chat feed is centered with a max-width of 800px to ensure line lengths for AI responses remain readable (approx. 70-80 characters per line).

## Elevation & Depth

Depth is achieved through **Ambient Shadows** and tonal layering rather than heavy borders.

- **Level 0 (Base):** #FFFFFF background.
- **Level 1 (Cards/Surfaces):** A subtle 1px border in #F1F5F9 with a soft shadow (0px 4px 20px rgba(15, 23, 42, 0.04)).
- **Level 2 (Active/Floating):** Used for the floating input bar and active modals. Shadow: 0px 12px 32px rgba(15, 23, 42, 0.08).
- **Interactive States:** On hover, cards should lift slightly (translateY -2px) and the shadow should increase in diffusion.

## Shapes

The design system employs a **Rounded** philosophy (0.5rem / 8px base) to soften the technical nature of financial data. 

- **Standard Elements:** 8px (0.5rem) for buttons and input fields.
- **Container Elements:** 16px (1rem) for main dashboard cards and chat bubbles.
- **Large Sections:** 24px (1.5rem) for main layout wrappers or empty state hero containers.

## Components

### Buttons
- **Primary:** Solid #0F172A with white text. 8px radius. High-contrast and authoritative.
- **Secondary:** Ghost style with #F1F5F9 background and #0F172A text.

### Message Bubbles
- **User:** Deep Slate (#0F172A) with white text. Right-aligned.
- **AI Assistant:** White background with a subtle #F1F5F9 border. Left-aligned. Use a distinct icon or "sparkle" subtle glow to denote AI-generated content.

### Floating Input
The primary AI prompt bar should be detached from the bottom of the viewport, appearing as a floating pill-shaped or 16px-radius container with a Level 2 elevation.

### Data Cards
Financial metrics should be housed in Level 1 cards. When a metric is positive, the top border or a small sparkline should utilize the Emerald Green (#10B981) accent.

### Chips & Tags
Use for categories like "Investing," "Savings," or "Risk." These should have a 100px (pill) radius and use low-saturation background tints of the primary colors (e.g., #F1F5F9).