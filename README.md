# MapBiomas Mosaic

This repository contains scripts used to generate annual satellite image mosaics and prepare inputs for land use and land cover (LULC) classification in the context of the MapBiomas project.

---

## 📌 Overview

These repository integrates Earth observation data to produce consistent annual mosaics that support land use and land cover classification across Brazil. These mosaics are built using surface reflectance images from the Landsat mission and are enriched with spectral and temporal metrics to enhance classification performance.

---

## 💡 Methodology

The workflow includes:

- Selection of cloud-free imagery from Landsat missions (TM, ETM+, OLI).
- Generation of annual mosaics using median, percentile, and other compositing strategies.
- Extraction of per-pixel metrics such as:
  - Spectral indices (e.g., NDVI, NBR, SAVI),
  - Spectral mixture analysis (SMA),
  - Temporal statistics (e.g., mean, min, variance),
  - Seasonal and phenological indicators.

After metrics are computed, machine learning algorithms (e.g., Random Forest) are applied to classify LULC. Temporal consistency is enforced by applying rule-based filters to correct spurious class transitions over time.

This approach follows the principles outlined in the official Algorithm Theoretical Basis Documents (ATBDs) from the MapBiomas initiative.

---

## 📚 References

- [MapBiomas Project](https://mapbiomas.org/)
- [Google Earth Engine](https://earthengine.google.com/)
- [MapBiomas ATBDs – Algorithm Theoretical Basis Documents](https://brasil.mapbiomas.org/download-dos-atbds-com-metodo-detalhado/D)

---

## 🤝 Contributing

We welcome contributions! You can:

- Open issues to report bugs or suggest improvements;
- Submit pull requests with new features or enhancements;
- Fork and adapt this repository for your own remote sensing workflows.

---

> This repository is part of the broader effort to improve environmental and land monitoring through open data, remote sensing, and collaborative science.
