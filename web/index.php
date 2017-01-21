<?php
Include "php_functions/templating.php";
Include "templates/navbar.php";
initialize_session();
process_global_gets();
echo load_header("home");
?>


<body>
	
	<?php

        if (isset($_SESSION['token'])) {
            echo "Logged In";
        }

        generateDefaultHeaderNavbar('index.php')->echo();
        generateFooter('index.php')->echoWithContainer();

	?>

</body>