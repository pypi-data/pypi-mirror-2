/* */

function handleUpload(upload) {
   if ($(upload).parent().find('input[type=file]').length < maxUploads)
      $(upload).before($(upload).clone()).before('<br />')
}