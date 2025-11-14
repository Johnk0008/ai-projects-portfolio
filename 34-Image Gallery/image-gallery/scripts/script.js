class ImageGallery {
    constructor() {
        this.images = [
            {
                src: 'https://picsum.photos/400/300?random=1',
                title: 'Mountain Landscape',
                description: 'Beautiful mountain view with clear sky',
                category: 'nature'
            },
            {
                src: 'https://picsum.photos/400/300?random=2',
                title: 'Modern Architecture',
                description: 'Contemporary building design',
                category: 'architecture'
            },
            {
                src: 'https://picsum.photos/400/300?random=3',
                title: 'AI Technology',
                description: 'Futuristic technology concept',
                category: 'technology'
            },
            {
                src: 'https://picsum.photos/400/300?random=4',
                title: 'Abstract Art',
                description: 'Colorful abstract painting',
                category: 'art'
            },
            {
                src: 'https://picsum.photos/400/300?random=5',
                title: 'Forest Path',
                description: 'Serene forest pathway',
                category: 'nature'
            },
            {
                src: 'https://picsum.photos/400/300?random=6',
                title: 'Urban Skyline',
                description: 'City skyline at dusk',
                category: 'architecture'
            },
            {
                src: 'https://picsum.photos/400/300?random=7',
                title: 'Neural Network',
                description: 'AI neural network visualization',
                category: 'technology'
            },
            {
                src: 'https://picsum.photos/400/300?random=8',
                title: 'Digital Painting',
                description: 'Modern digital artwork',
                category: 'art'
            },
            {
                src: 'https://picsum.photos/400/300?random=9',
                title: 'Ocean Waves',
                description: 'Powerful ocean waves crashing',
                category: 'nature'
            },
            {
                src: 'https://picsum.photos/400/300?random=10',
                title: 'Historic Building',
                description: 'Ancient architectural marvel',
                category: 'architecture'
            },
            {
                src: 'https://picsum.photos/400/300?random=11',
                title: 'Robotics',
                description: 'Advanced robotics technology',
                category: 'technology'
            },
            {
                src: 'https://picsum.photos/400/300?random=12',
                title: 'Surreal Art',
                description: 'Dreamlike surreal composition',
                category: 'art'
            }
        ];

        this.currentImageIndex = 0;
        this.activeFilter = 'all';
        
        this.init();
    }

    init() {
        this.renderGallery();
        this.setupEventListeners();
    }

    renderGallery() {
        const galleryContainer = document.querySelector('.gallery-container');
        const filteredImages = this.activeFilter === 'all' 
            ? this.images 
            : this.images.filter(img => img.category === this.activeFilter);

        galleryContainer.innerHTML = filteredImages.map((image, index) => `
            <div class="gallery-item" data-index="${index}" data-category="${image.category}">
                <img src="${image.src}" alt="${image.title}" loading="lazy">
                <div class="image-overlay">
                    <div class="image-title">${image.title}</div>
                    <span class="image-category">${image.category}</span>
                </div>
            </div>
        `).join('');
    }

    setupEventListeners() {
        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.activeFilter = e.target.dataset.filter;
                this.renderGallery();
                this.setupImageClickListeners();
            });
        });

        // Lightbox navigation
        document.querySelector('.close-btn').addEventListener('click', () => this.closeLightbox());
        document.querySelector('.prev-btn').addEventListener('click', () => this.navigate(-1));
        document.querySelector('.next-btn').addEventListener('click', () => this.navigate(1));
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (document.getElementById('lightbox').style.display === 'block') {
                if (e.key === 'Escape') this.closeLightbox();
                if (e.key === 'ArrowLeft') this.navigate(-1);
                if (e.key === 'ArrowRight') this.navigate(1);
            }
        });

        // Close lightbox when clicking outside image
        document.getElementById('lightbox').addEventListener('click', (e) => {
            if (e.target.id === 'lightbox') this.closeLightbox();
        });

        this.setupImageClickListeners();
    }

    setupImageClickListeners() {
        document.querySelectorAll('.gallery-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const index = parseInt(item.dataset.index);
                this.openLightbox(index);
            });
        });
    }

    openLightbox(index) {
        this.currentImageIndex = index;
        const image = this.images[index];
        
        document.getElementById('lightbox-img').src = image.src;
        document.getElementById('image-title').textContent = image.title;
        document.getElementById('image-description').textContent = image.description;
        document.getElementById('lightbox').style.display = 'block';
        
        // Add fade-in animation
        document.getElementById('lightbox').style.animation = 'fadeIn 0.3s ease';
    }

    closeLightbox() {
        document.getElementById('lightbox').style.display = 'none';
    }

    navigate(direction) {
        const filteredImages = this.activeFilter === 'all' 
            ? this.images 
            : this.images.filter(img => img.category === this.activeFilter);
        
        this.currentImageIndex += direction;
        
        if (this.currentImageIndex < 0) {
            this.currentImageIndex = filteredImages.length - 1;
        } else if (this.currentImageIndex >= filteredImages.length) {
            this.currentImageIndex = 0;
        }
        
        // Find the actual index in the main images array
        const currentImage = filteredImages[this.currentImageIndex];
        const actualIndex = this.images.findIndex(img => img.src === currentImage.src);
        
        this.openLightbox(actualIndex);
    }
}

// Initialize the gallery when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ImageGallery();
});

// Add loading animation
window.addEventListener('load', () => {
    document.body.style.opacity = '1';
});

document.body.style.opacity = '0';
document.body.style.transition = 'opacity 0.5s ease';