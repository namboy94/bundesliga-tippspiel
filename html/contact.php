<?php
Include "functions/templating.php";
initialize_session();
process_global_gets();
echo load_header("contact");
?>

<body>
	
	<?php

		echo load_navbar("contact");
		echo load_html("templates/contact_body.html");
		echo load_html("templates/footer.html");

	?>

</body>
