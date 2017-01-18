<?php
Include "php_functions/templating.php";
initialize_session();
process_global_gets();
echo load_header("home");
?>


<body>
	
	<?php

		echo load_navbar("home");
		echo load_html("html_content/templates/footer.html");

	?>

</body>