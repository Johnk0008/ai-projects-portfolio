class MusicPlayer {
    constructor() {
        this.audio = document.getElementById('audio-player');
        this.playBtn = document.getElementById('play-btn');
        this.prevBtn = document.getElementById('prev-btn');
        this.nextBtn = document.getElementById('next-btn');
        this.shuffleBtn = document.getElementById('shuffle-btn');
        this.repeatBtn = document.getElementById('repeat-btn');
        this.progressBar = document.getElementById('progress-bar');
        this.progress = document.getElementById('progress');
        this.volumeBar = document.getElementById('volume-bar');
        this.volumeLevel = document.getElementById('volume-level');
        this.currentTimeEl = document.getElementById('current-time');
        this.totalTimeEl = document.getElementById('total-time');
        this.songTitle = document.getElementById('song-title');
        this.songArtist = document.getElementById('song-artist');
        this.songDuration = document.getElementById('song-duration');
        this.playlistEl = document.getElementById('playlist');
        this.albumArt = document.querySelector('.album-art');

        this.songs = [];
        this.currentSongIndex = 0;
        this.isPlaying = false;
        this.isShuffled = false;
        this.repeatMode = 0; // 0: no repeat, 1: repeat all, 2: repeat one
        this.originalPlaylist = [];

        this.init();
    }

    async init() {
        await this.loadSongs();
        this.setupEventListeners();
        this.updatePlaylist();
        this.loadSong(0);
    }

    async loadSongs() {
        try {
            const response = await fetch('http://localhost:5000/api/songs');
            this.songs = await response.json();
            this.originalPlaylist = [...this.songs];
        } catch (error) {
            console.error('Error loading songs:', error);
            // Fallback to demo songs if backend is not available
            this.songs = [
                {
                    id: 1,
                    title: "Demo Song 1",
                    artist: "Demo Artist 1",
                    file: "demo1.mp3",
                    duration: "3:45"
                },
                {
                    id: 2,
                    title: "Demo Song 2",
                    artist: "Demo Artist 2",
                    file: "demo2.mp3",
                    duration: "4:20"
                },
                {
                    id: 3,
                    title: "Demo Song 3",
                    artist: "Demo Artist 3",
                    file: "demo3.mp3",
                    duration: "3:15"
                }
            ];
            this.originalPlaylist = [...this.songs];
        }
    }

    setupEventListeners() {
        // Play/Pause
        this.playBtn.addEventListener('click', () => this.togglePlay());

        // Previous/Next
        this.prevBtn.addEventListener('click', () => this.previousSong());
        this.nextBtn.addEventListener('click', () => this.nextSong());

        // Shuffle
        this.shuffleBtn.addEventListener('click', () => this.toggleShuffle());

        // Repeat
        this.repeatBtn.addEventListener('click', () => this.toggleRepeat());

        // Progress bar
        this.progressBar.addEventListener('click', (e) => this.setProgress(e));

        // Volume control
        this.volumeBar.addEventListener('click', (e) => this.setVolume(e));

        // Audio events
        this.audio.addEventListener('loadedmetadata', () => this.updateTime());
        this.audio.addEventListener('timeupdate', () => this.updateProgress());
        this.audio.addEventListener('ended', () => this.songEnded());

        // Keyboard controls
        document.addEventListener('keydown', (e) => this.handleKeyPress(e));
    }

    loadSong(index) {
        if (this.songs.length === 0) return;

        this.currentSongIndex = index;
        const song = this.songs[index];
        
        // Try to load from backend, fallback to empty audio if not available
        const audioUrl = `http://localhost:5000/music/${song.file}`;
        this.audio.src = audioUrl;
        
        this.songTitle.textContent = song.title;
        this.songArtist.textContent = song.artist;
        this.songDuration.textContent = song.duration;

        this.updatePlaylist();
        
        // Load the audio and update total time when metadata is loaded
        this.audio.addEventListener('loadedmetadata', () => {
            this.totalTimeEl.textContent = this.formatTime(this.audio.duration);
        }, { once: true });

        if (this.isPlaying) {
            this.playSong();
        }
    }

    togglePlay() {
        if (this.isPlaying) {
            this.pauseSong();
        } else {
            this.playSong();
        }
    }

    playSong() {
        this.audio.play().then(() => {
            this.isPlaying = true;
            this.playBtn.innerHTML = '<i class="fas fa-pause"></i>';
            this.albumArt.classList.add('playing');
        }).catch(error => {
            console.error('Error playing audio:', error);
        });
    }

    pauseSong() {
        this.audio.pause();
        this.isPlaying = false;
        this.playBtn.innerHTML = '<i class="fas fa-play"></i>';
        this.albumArt.classList.remove('playing');
    }

    nextSong() {
        let nextIndex = this.currentSongIndex + 1;
        if (nextIndex >= this.songs.length) {
            if (this.repeatMode === 1) {
                nextIndex = 0;
            } else {
                return;
            }
        }
        this.loadSong(nextIndex);
        if (this.isPlaying) {
            this.playSong();
        }
    }

    previousSong() {
        let prevIndex = this.currentSongIndex - 1;
        if (prevIndex < 0) {
            if (this.repeatMode === 1) {
                prevIndex = this.songs.length - 1;
            } else {
                return;
            }
        }
        this.loadSong(prevIndex);
        if (this.isPlaying) {
            this.playSong();
        }
    }

    toggleShuffle() {
        this.isShuffled = !this.isShuffled;
        this.shuffleBtn.style.color = this.isShuffled ? '#667eea' : '#666';

        if (this.isShuffled) {
            // Shuffle the playlist
            this.songs = [...this.originalPlaylist].sort(() => Math.random() - 0.5);
        } else {
            // Restore original order
            this.songs = [...this.originalPlaylist];
            // Find current song in original playlist
            const currentSong = this.songs[this.currentSongIndex];
            this.currentSongIndex = this.originalPlaylist.findIndex(song => song.id === currentSong.id);
        }
        this.updatePlaylist();
    }

    toggleRepeat() {
        this.repeatMode = (this.repeatMode + 1) % 3;
        const repeatIcons = ['fa-redo', 'fa-list', 'fa-repeat'];
        const repeatTitles = ['No Repeat', 'Repeat All', 'Repeat One'];
        
        this.repeatBtn.innerHTML = `<i class="fas ${repeatIcons[this.repeatMode]}"></i>`;
        this.repeatBtn.title = repeatTitles[this.repeatMode];
        this.repeatBtn.style.color = this.repeatMode > 0 ? '#667eea' : '#666';
    }

    setProgress(e) {
        const rect = this.progressBar.getBoundingClientRect();
        const percent = (e.clientX - rect.left) / rect.width;
        this.audio.currentTime = percent * this.audio.duration;
    }

    setVolume(e) {
        const rect = this.volumeBar.getBoundingClientRect();
        const percent = (e.clientX - rect.left) / rect.width;
        this.audio.volume = Math.max(0, Math.min(1, percent));
        this.volumeLevel.style.width = `${percent * 100}%`;
    }

    updateProgress() {
        if (this.audio.duration) {
            const percent = (this.audio.currentTime / this.audio.duration) * 100;
            this.progress.style.width = `${percent}%`;
            this.currentTimeEl.textContent = this.formatTime(this.audio.currentTime);
        }
    }

    updateTime() {
        this.totalTimeEl.textContent = this.formatTime(this.audio.duration);
    }

    formatTime(seconds) {
        if (isNaN(seconds)) return '0:00';
        
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }

    songEnded() {
        if (this.repeatMode === 2) {
            // Repeat one
            this.audio.currentTime = 0;
            this.playSong();
        } else {
            this.nextSong();
        }
    }

    updatePlaylist() {
        this.playlistEl.innerHTML = '';
        this.songs.forEach((song, index) => {
            const item = document.createElement('div');
            item.className = `playlist-item ${index === this.currentSongIndex ? 'playing' : ''}`;
            item.innerHTML = `
                <span class="song-number">${index + 1}</span>
                <div class="song-details">
                    <h4>${song.title}</h4>
                    <p>${song.artist}</p>
                </div>
                <span class="song-duration">${song.duration}</span>
            `;
            item.addEventListener('click', () => {
                this.loadSong(index);
                if (this.isPlaying) {
                    this.playSong();
                }
            });
            this.playlistEl.appendChild(item);
        });
    }

    handleKeyPress(e) {
        switch(e.code) {
            case 'Space':
                e.preventDefault();
                this.togglePlay();
                break;
            case 'ArrowRight':
                this.nextSong();
                break;
            case 'ArrowLeft':
                this.previousSong();
                break;
            case 'ArrowUp':
                this.audio.volume = Math.min(1, this.audio.volume + 0.1);
                this.volumeLevel.style.width = `${this.audio.volume * 100}%`;
                break;
            case 'ArrowDown':
                this.audio.volume = Math.max(0, this.audio.volume - 0.1);
                this.volumeLevel.style.width = `${this.audio.volume * 100}%`;
                break;
        }
    }
}

// Initialize the music player when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new MusicPlayer();
});