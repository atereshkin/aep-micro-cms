$(document).ready(
  function()
  {
    $('.editable .rich').editable('.', { 'type' : 'wym',
					 'submit' : 'ok',
					 'wym' : { 'basePath' : '',
						   'loadSkin' : false,
						   'updateSelector' : 'button'}});

     $('.editable .string').editable('.');

  });
