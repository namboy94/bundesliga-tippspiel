<?php
Include "functions/templating.php";
initialize_session();
echo load_header("contact");
?>

<body>
	
	<?php

		echo load_navbar("contact");
		echo load_html("templates/contact_body.html");

	?>

</body>
