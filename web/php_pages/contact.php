<?php
Include "php_functions/templating.php";
initialize_session();
process_global_gets();
echo load_header("contact");
?>

<body>
	
	<?php

		echo load_navbar("contact");
		echo load_html("html_content/contact_body.html");
		echo load_html("html_content/templates/footer.html");

	?>

</body>
