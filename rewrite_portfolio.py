import re

old_html = ""
import subprocess
result = subprocess.run(['git', 'show', 'HEAD:portfolio.html'], capture_output=True, text=True)
old_html = result.stdout

# Categories and their filter strings
# logo-designs -> img/portfolio/Logos/...
# expo-invite -> img/portfolio/expo-invite/...
# standee-designs -> img/portfolio/standee-designs/...
# banner-designs -> img/portfolio/banners/...
# news-paper -> img/portfolio/news-paper/...

images = re.findall(r'<img src="(img/portfolio/[^"]+)"', old_html)
# Remove duplicates
seen = set()
unique_images = []
for img in images:
    if img not in seen:
        seen.add(img)
        unique_images.append(img)

def get_category_info(img_src):
    if 'Logos' in img_src: return ('logo-designs', 'Logo Design')
    if 'expo-invite' in img_src: return ('expo-invite', 'Expo Invite')
    if 'standee-designs' in img_src: return ('standee-designs', 'Standee Design')
    if 'banners' in img_src: return ('banner-designs', 'Banner Design')
    if 'news-paper' in img_src: return ('news-paper', 'News Paper Design')
    return ('other', 'Other')

grid_html = ""
for i, img in enumerate(unique_images):
    cat_class, cat_name = get_category_info(img)
    title = f"Project {i+1}"
    grid_html += f"""
                <div class="v3-portfolio-item filter-item {cat_class}">
                    <img src="{img}" alt="{cat_name}">
                    <div class="v3-portfolio-overlay">
                        <h4>{cat_name}</h4>
                        <p>{cat_class.replace('-', ' ').title()}</p>
                    </div>
                </div>
"""

new_portfolio = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Portfolio | Shweta Jadhav</title>
    <meta name="description" content="Portfolio of Shweta Jadhav - Graphic Designer.">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- v3 Redesign CSS -->
    <link rel="stylesheet" href="css/v3-redesign.css">
</head>
<body>
    <!-- Top Navigation -->
    <nav class="v3-navbar">
        <div class="v3-nav-container">
            <a href="index.html" class="v3-logo">
                <img src="img/logo/logo2.png" alt="Logo" style="filter: brightness(0) invert(1);"> <span>.</span>
            </a>
            <ul class="v3-nav-links">
                <li><a href="index.html">Home</a></li>
                <li><a href="portfolio.html" class="active">Portfolio</a></li>
                <li><a href="about.html">About</a></li>
                <li><a href="services.html">Services</a></li>
                <li><a href="contact.html">Contact</a></li>
            </ul>
            <div class="v3-social-nav">
                <a href="https://www.linkedin.com" target="_blank"><i class="fab fa-linkedin-in"></i></a>
                <a href="https://www.behance.net/shwetajadhav11" target="_blank"><i class="fab fa-behance"></i></a>
            </div>
            <button class="v3-menu-toggle"><i class="fas fa-bars"></i></button>
        </div>
    </nav>
    <main class="v3-main-content">
        <section class="v3-container">
            <div class="v3-page-header">
                <h2 class="v3-page-title">Selected <span>Works</span></h2>
                <span class="v3-page-subtitle">My Portfolio</span>
            </div>
            <div class="v3-portfolio-filters">
                <button class="v3-filter-btn active" onclick="filterSelection('all')">All</button>
                <button class="v3-filter-btn" onclick="filterSelection('logo-designs')">Logo Design</button>
                <button class="v3-filter-btn" onclick="filterSelection('expo-invite')">Expo Invite</button>
                <button class="v3-filter-btn" onclick="filterSelection('standee-designs')">Standees</button>
                <button class="v3-filter-btn" onclick="filterSelection('banner-designs')">Banners</button>
                <button class="v3-filter-btn" onclick="filterSelection('news-paper')">News Paper</button>
            </div>
            <div class="v3-portfolio-grid">
{grid_html}
            </div>
        </section>
    </main>
    <script>
        const toggle = document.querySelector('.v3-menu-toggle');
        const links = document.querySelector('.v3-nav-links');
        toggle.addEventListener('click', () => {{
            if(links.style.display === 'flex') {{
                links.style.display = 'none';
            }} else {{
                links.style.display = 'flex';
                links.style.flexDirection = 'column';
                links.style.position = 'absolute';
                links.style.top = '80px';
                links.style.left = '0';
                links.style.width = '100%';
                links.style.background = '#09090b';
                links.style.padding = '20px';
            }}
        }});
        function filterSelection(c) {{
            var x, i;
            x = document.getElementsByClassName("filter-item");
            if (c == "all") c = "";
            for (i = 0; i < x.length; i++) {{
                w3RemoveClass(x[i], "show");
                if (x[i].className.indexOf(c) > -1) w3AddClass(x[i], "show");
            }}
            var btns = document.getElementsByClassName("v3-filter-btn");
            for (i = 0; i < btns.length; i++) {{
                btns[i].className = btns[i].className.replace(" active", "");
                if(event && event.currentTarget === btns[i]) {{
                    btns[i].className += " active";
                }}
            }}
        }}
        function w3AddClass(element, name) {{
            var i, arr1, arr2;
            arr1 = element.className.split(" ");
            arr2 = name.split(" ");
            for (i = 0; i < arr2.length; i++) {{
                if (arr1.indexOf(arr2[i]) == -1) {{element.className += " " + arr2[i];}}
            }}
        }}
        function w3RemoveClass(element, name) {{
            var i, arr1, arr2;
            arr1 = element.className.split(" ");
            arr2 = name.split(" ");
            for (i = 0; i < arr2.length; i++) {{
                while (arr1.indexOf(arr2[i]) > -1) {{
                    arr1.splice(arr1.indexOf(arr2[i]), 1);     
                }}
            }}
            element.className = arr1.join(" ");
        }}
        const style = document.createElement('style');
        style.innerHTML = `
            .filter-item {{ display: none; }}
            .filter-item.show {{ display: block; }}
        `;
        document.head.appendChild(style);
        filterSelection("all");
    </script>
</body>
</html>
"""

with open('portfolio.html', 'w') as f:
    f.write(new_portfolio)

