$(document).ready(
  function()
  {
    $('.editable .rich').editable('.', { 'type' : 'wym',
					 'submit' : 'OKs',
					 'cancel' : 'Cancel',
					 'wym' : { 'basePath' : '',
						   'loadSkin' : false,
						   'updateSelector' : 'button'}});

     $('.editable .string').editable('.');

  });
