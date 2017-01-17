<?php
Include "functions/templating.php";
initialize_session();
echo load_header("Bundesliga Tippspiel - Contact");
?>


<body>
	
	<?php

		echo load_navbar("contact")

	?>

	<div class="container">

		<div class="jumbotron">
			<h1>Contact</h1>
		</div>

		<div class="row">

			<div class="col-sm-4">
				<h2>@$admin_contact_title</h2>
				<p><a href="mailto:@!DEV_EMAIL_ADDR">@!DEV_EMAIL_ADDR</a></p>
			</div>

		</div>

	</div>

</body>
