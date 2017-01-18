<?php
Include "php_functions/templating.php";
initialize_session();
process_global_gets();
echo load_header("signup");
?>


<body>

<?php

    echo load_navbar("signup");
    echo load_html("html_content/signup_body.html");
    echo load_html("html_content/templates/footer.html");

?>

</body>