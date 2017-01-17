<?php
Include "functions/templating.php";
initialize_session();
process_global_gets();
echo load_header("about");
?>


<body>
	
	<?php

		echo load_navbar("about")

	?>

</body>