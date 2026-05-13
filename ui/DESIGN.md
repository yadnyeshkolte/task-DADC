---
name: Gold-Standard BI
colors:
  surface: '#fbf9f8'
  surface-dim: '#dcd9d9'
  surface-bright: '#fbf9f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3f2'
  surface-container: '#f0eded'
  surface-container-high: '#eae8e7'
  surface-container-highest: '#e4e2e1'
  on-surface: '#1b1c1c'
  on-surface-variant: '#4d4635'
  inverse-surface: '#303030'
  inverse-on-surface: '#f3f0f0'
  outline: '#7f7663'
  outline-variant: '#d0c5af'
  surface-tint: '#735c00'
  primary: '#735c00'
  on-primary: '#ffffff'
  primary-container: '#d4af37'
  on-primary-container: '#554300'
  inverse-primary: '#e9c349'
  secondary: '#4e6073'
  on-secondary: '#ffffff'
  secondary-container: '#cfe2f9'
  on-secondary-container: '#526478'
  tertiary: '#546162'
  on-tertiary: '#ffffff'
  tertiary-container: '#a8b5b6'
  on-tertiary-container: '#3b4748'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffe088'
  primary-fixed-dim: '#e9c349'
  on-primary-fixed: '#241a00'
  on-primary-fixed-variant: '#574500'
  secondary-fixed: '#d1e4fb'
  secondary-fixed-dim: '#b5c8df'
  on-secondary-fixed: '#091d2e'
  on-secondary-fixed-variant: '#36485b'
  tertiary-fixed: '#d8e5e6'
  tertiary-fixed-dim: '#bcc9ca'
  on-tertiary-fixed: '#121e1f'
  on-tertiary-fixed-variant: '#3d494a'
  background: '#fbf9f8'
  on-background: '#1b1c1c'
  surface-variant: '#e4e2e1'
  primary-accent: '#D4AF37'
  text-main: '#333333'
  border-subtle: '#E9ECEF'
  well-background: '#F8F9FA'
typography:
  display:
    fontFamily: Manrope
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  h1:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  h2:
    fontFamily: Manrope
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-caps:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  data-tabular:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 12px
  md: 20px
  lg: 32px
  xl: 48px
  gutter: 24px
  margin: 32px
---

## Brand & Style
The design system is engineered for executive-level business intelligence. It prioritizes clarity, precision, and an air of established authority. The style is **Minimalist / Corporate**, leaning into high-quality white space to prevent data fatigue. 

The aesthetic avoids "techy" neon trends in favor of a sophisticated palette that mirrors premium physical stationery or high-end financial reports. There are no "edit-mode" artifacts like visible drag handles or grid dots; the interface feels finished, immutable, and trustworthy. The emotional response should be one of calm control over complex data.

## Colors
The palette is anchored by a professional gold/mustard primary accent used sparingly for key call-to-actions, active states, and critical data highlights. 

- **Primary (#D4AF37):** Used for "Aha!" moments in data—peak values, active filter states, and primary action buttons.
- **Surface Strategy:** The main dashboard canvas uses `#FFFFFF`. Subtle grouping and "well" containers use `#F8F9FA`.
- **Typography:** Primary text is `#333333` to ensure high legibility while remaining softer than pure black.
- **Semantic Colors:** Success (Green), Warning (Amber), and Danger (Red) should be desaturated to match the sophisticated tone of the gold accent.

## Typography
This design system utilizes **Manrope** for headlines to provide a modern, slightly geometric character, and **Inter** for data-heavy body and UI elements to ensure maximum legibility at small sizes.

Key rules:
- **Tabular Figures:** Always enable "tnum" (tabular numbers) for tables to ensure numerical columns align vertically.
- **Labels:** Use `label-caps` for table headers and small section titles to create a distinct visual break from data.
- **Hierarchy:** Use font weight rather than color shifts to denote importance, maintaining the `#333333` anchor for most text.

## Layout & Spacing
The layout follows a **Fluid Grid** model with a focus on "Data Density without Clutter." 

- **Dashboard Grid:** 12-column layout with 24px gutters. 
- **The "Breathable" Rule:** For every high-density data table, ensure the surrounding card container has a minimum of 20px (`md`) internal padding.
- **Modular Blocks:** Components should be grouped into logical cards. Related metrics (KPI sparks) use `sm` spacing, while distinct sections use `lg`.
- **Responsive:** On Tablet, the 12-column grid collapses to 6. On Mobile, it becomes a single column with horizontal scrolling enabled specifically for wide data tables.

## Elevation & Depth
This design system avoids heavy shadows. Depth is communicated through **Tonal Layers** and **Low-Contrast Outlines**.

- **Level 0 (Background):** `#FFFFFF` or `#F8F9FA`.
- **Level 1 (Cards):** `#FFFFFF` surface with a 1px border of `#E9ECEF`.
- **Level 2 (Dropdowns/Modals):** A very soft, diffused shadow (`0 4px 20px rgba(0,0,0,0.05)`) is used only for elements that temporarily float above the layout.
- **Hover States:** Subtle shift in background color (e.g., from `#FFFFFF` to `#F8F9FA`) rather than a shadow "lift."

## Shapes
The shape language is **Soft**. 

- **Standard Elements:** Buttons, input fields, and checkboxes use a `0.25rem` (4px) radius. This provides a professional, "exact" feel.
- **Large Containers:** Dashboard cards use `rounded-lg` (8px) to soften the overall appearance of the page.
- **Interactive Indicators:** Range slider handles and radio buttons remain circular to clearly denote their physical affordance.

## Components
Consistent implementation of components is vital for data integrity.

- **Tables:** - Use zebra striping with `#F8F9FA` on even rows. 
  - Borders should be horizontal-only to emphasize the flow of data. 
  - Headers are sticky and use the `label-caps` typography style.
- **Filter Dropdowns:** - Use a clean, border-only style. 
  - The "Active" state is indicated by a 2px bottom border in the primary gold (`#D4AF37`) and bolded text.
- **Dual-Handle Range Sliders:** - The track is `#E9ECEF`. 
  - The active range is `#D4AF37`. 
  - Handles are white with a 1px border of the primary gold.
- **Buttons:** - Primary buttons are solid `#D4AF37` with white text. 
  - Secondary buttons are ghost-style with `#333333` text and a light gray border.
- **Input Fields:** - No background color; use a 1px border of `#E9ECEF`. 
  - On focus, the border transitions to the primary gold.
- **KPI Cards:** - Feature a large `display` metric, a small sparkline in the primary gold, and a comparison label (e.g., "+12% vs last month").