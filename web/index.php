<?php

include_once "php_functions/templating.php";
include_once "templates/navbar.php";

initialize_session();
process_global_gets();
echo load_header("home");
?>


<body>
	
	<?php

        generateDefaultHeaderNavbar('index.php')->echo();
        generateFooter('index.php')->echoWithContainer();

	?>

</body>