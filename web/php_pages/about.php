<?php
Include "php_functions/templating.php";
initialize_session();
process_global_gets();
echo load_header("about");
?>


<body>
	
	<?php

		echo load_navbar("about");
		echo load_html("html_content/about_body.web");
		echo load_html("html_content/templates/footer.web");

	?>

</body>