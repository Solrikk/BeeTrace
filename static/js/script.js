
document.addEventListener('DOMContentLoaded', () => {
    const previewImage = (input, previewId) => {
        const preview = document.getElementById(previewId);
        const file = input.files[0];
        
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                preview.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
            };
            reader.readAsDataURL(file);
        }
    };

    document.getElementById('imageA').addEventListener('change', function() {
        previewImage(this, 'previewA');
    });

    document.getElementById('imageB').addEventListener('change', function() {
        previewImage(this, 'previewB');
    });

    document.getElementById('upload-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const button = e.target.querySelector('.submit-btn');
        const resultContainer = document.getElementById('result');
        
        // Validate files
        const imageA = document.getElementById('imageA').files[0];
        const imageB = document.getElementById('imageB').files[0];
        if (!imageA || !imageB) {
            alert('Please select both images');
            return;
        }

        // Show loading state
        button.disabled = true;
        button.textContent = 'Processing...';
        resultContainer.innerHTML = 'Processing images...';
        
        const formData = new FormData(e.target);
        
        try {
            const response = await fetch('/match-features/', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const blob = await response.blob();
            const imageUrl = URL.createObjectURL(blob);
            resultContainer.innerHTML = `<img src="${imageUrl}" alt="Matched Features">`;
        } catch (error) {
            console.error('Error:', error);
            resultContainer.innerHTML = 'Error processing images. Please try again.';
        } finally {
            button.disabled = false;
            button.textContent = 'Match Features';
        }
    });
});
