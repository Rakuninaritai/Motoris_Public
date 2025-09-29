$(document).ready(function() {
  $('#id_images').on('change', function(event) {
    var files = event.target.files;
    var previewContainer = $('.image-preview');
    previewContainer.empty();

    var selectedFiles = Array.from(files);

    selectedFiles.forEach(function(file) {
      var reader = new FileReader();
      reader.onload = function(e) {
        previewContainer.append(`
          <div class="image-preview-item">
            <img src="${e.target.result}" alt="Image preview" class="img-thumbnail" width="100">
          </div>
        `);
      };
      reader.readAsDataURL(file);
    });
  });
});