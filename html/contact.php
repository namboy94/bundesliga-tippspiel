<?php
Include "functions/templating.php";
initialize_session();
echo load_header("Bundesliga Tippspiel - Contact");
?>

<body>
	
	<?php

		echo load_navbar("contact");
		echo load_html("templates/contact_body.html");

	?>

</body>
