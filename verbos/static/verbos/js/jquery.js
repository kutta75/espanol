		// gestion des data locales
		// ici on recoit une liste composéee de couple "nom du modele" , idi di modele 
		// on teste si le champ nomdumodel-id exite en local storage 
		// si non , on le crée et on l'initiale avec la valeur texte a "true" ( qui n'est pas un booleen !!)
		function initlocal(mylist) {
			mytype= typeof mylist;
			console.log("dans la fonction initlocal");
			for (var i=0 ; i < mylist.length; i++ ) {
				console.log(mylist[i]);
				myvar = mylist[i][0] + "-" + mylist[i][1];
				if (!localStorage.getItem(myvar)) {
					localStorage.setItem(myvar,"true");
					console.log('dans init'+ myvar );
				};
			}
		}

		function checklocal(mylist) {
			// ici on gere les bloc de check box pour cocher - decocher en une fois 
			// le bloc de selection globale doit  avoir un name de "checktodos" et les sous 
			// boite doivent avoir pour naem le data-type du la boite globale 
			// ouf 

			for (var i=0 ; i < mylist.length; i++ ) {
				myvar = mylist[i][0] + "-" + mylist[i][1];
				myvarvalue = false; 
				if ( localStorage.getItem(myvar) == "true" ) {
					myvarvalue=true;
				};
			console.log(myvar + " = " + myvarvalue);
			myvar="#"+ myvar
			document.querySelector(myvar).checked = myvarvalue ;
		}
		}	
				

