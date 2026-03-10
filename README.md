# Change Will Happen - Haiti Medical Mission Website

A modern, professional website for documenting and promoting medical missions to Haiti.

## Project Structure

```
haiti-mission-site/
├── index.html          # Main HTML file
├── styles.css          # All styling
├── script.js           # JavaScript for interactivity
├── images/             # Image directory
│   ├── hero-main.jpg
│   ├── hero-secondary.jpg
│   ├── gallery-1.jpg through gallery-6.jpg
└── README.md           # This file
```

## Features

✨ **Professional Design**
- Modern, clean layout with professional color scheme
- Responsive design (works on desktop, tablet, mobile)
- Smooth animations and transitions
- Accessibility-friendly

🖼️ **Image Gallery**
- Beautiful lightbox gallery with keyboard navigation (arrow keys, ESC)
- Smooth zoom effects on hover
- Responsive grid layout

📱 **Responsive**
- Mobile-first design approach
- Optimized for all screen sizes
- Touch-friendly navigation

💰 **Donation Integration**
- Ready for PayPal integration
- Clean donation form
- Email verification

🎬 **Video Integration**
- Embedded YouTube videos
- Responsive video players

## Getting Started

### 1. Download the Files

All files are included in this folder:
- `index.html`
- `styles.css`
- `script.js`
- Create an `images/` folder

### 2. Download Your Images

You need to download the images from your Wix site and add them to the `images/` folder:

**Required images:**
- `hero-main.jpg` - Main hero image (Dr Ferdinand & Arihunt)
- `hero-secondary.jpg` - Story section image (Dr Pascale Ferdinand & Avni)
- `gallery-1.jpg through gallery-6.jpg` - Gallery images (6 images total)

**To download images from Wix:**
1. Go to your original Wix page
2. Right-click on each image → "Save image as..."
3. Save them to the `images/` folder with the names above

### 3. Deploy to Netlify

#### Option A: Using Netlify Drop (Easiest)
1. Go to [netlify.com/drop](https://netlify.com/drop)
2. Drag and drop your entire `haiti-mission-site` folder
3. Your site goes live instantly!

#### Option B: Connect GitHub (Recommended)
1. Create a GitHub account (free)
2. Create a new repository called `haiti-mission`
3. Upload all files to the repository
4. Go to [netlify.com](https://netlify.com)
5. Click "New site from Git" → Choose your repository
6. Deploy!

#### Option C: Deploy via Command Line
1. Install Node.js
2. Install Netlify CLI: `npm install -g netlify-cli`
3. In your project folder, run: `netlify deploy`
4. Follow the prompts
5. Your site will be live!

### 4. Custom Domain (Optional)

In Netlify dashboard:
1. Go to "Domain settings"
2. Add your custom domain (changewillhappen.org)
3. Point DNS records to Netlify

## Customization Guide

### Update Colors
Edit the CSS variables at the top of `styles.css`:
```css
:root {
    --primary-color: #2c5aa0;      /* Main blue */
    --secondary-color: #e74c3c;    /* Red accent */
    --accent-color: #3498db;       /* Light blue */
}
```

### Update Content
Edit the HTML in `index.html`:
- Change section titles, paragraphs, links
- Update video links (YouTube embed URLs)
- Modify navigation menu items

### Add/Remove Gallery Images
In `index.html`, the gallery section has 6 image slots. To add more:
```html
<div class="gallery-item" data-lightbox="haiti-2018">
    <img src="images/gallery-7.jpg" alt="Description" loading="lazy">
    <div class="gallery-overlay">
        <span class="zoom-icon">🔍</span>
    </div>
</div>
```

### Integrate PayPal Donations
Currently, the donation form shows an alert. To add real PayPal:

1. Get your PayPal Business Account
2. In `script.js`, modify the `showDonationSuccess()` function
3. Redirect to PayPal with the amount:
```javascript
window.location.href = `https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=YOUR_PAYPAL_EMAIL&item_name=Donation&amount=${amount}&currency_code=USD&return=${window.location.href}`;
```

## File Size & Performance

- HTML: ~15 KB
- CSS: ~20 KB
- JavaScript: ~5 KB
- **Total (without images): ~40 KB** - Super fast!

Images should be:
- Compressed (use [tinypng.com](https://tinypng.com) for free compression)
- 1-2 MB per image is fine for web
- JPG format for photos, PNG for graphics

## Browser Support

Works on:
- Chrome, Firefox, Safari, Edge (all modern versions)
- Mobile browsers (iOS Safari, Chrome Mobile)
- Internet Explorer 11+ (with some limitations)

## SEO & Analytics

### Add Google Analytics
Add this before `</body>` in `index.html`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_ID');
</script>
```

### Meta Tags for SEO
Already included in `index.html`:
- Title tag
- Viewport meta
- (Add description, keywords as needed)

## Maintenance

- Update images if needed (keep same filenames)
- Update text content directly in HTML
- No database or backend needed
- Entirely static site = very secure & fast

## Support & Questions

For deployment issues:
- [Netlify Docs](https://docs.netlify.com)
- [HTML/CSS Help](https://www.w3schools.com)

## Future Enhancements

Consider adding:
- [ ] Blog section for mission updates
- [ ] Volunteer signup form
- [ ] Newsletter subscription
- [ ] Multi-language support
- [ ] Instagram feed integration
- [ ] Team member profiles
- [ ] Photo slideshow transitions

---

**Built with ❤️ for Change Will Happen**
