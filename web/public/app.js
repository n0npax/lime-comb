function logoutFirebase() {
    firebase.auth().signOut().then(function() {
      // Sign-out successful.
    }, function(error) {
      alert(error)
    });
  }
  
  var firebaseuiAuthContainer = document.getElementById("firebaseui-auth-container");
  var userAuthContainer = document.getElementById("user-auth-container");
  var userNameContainer = document.getElementById("userNameContainer");
  var mainContainer = document.getElementById("main");
  var CurrGPGTextAreaContainer = document.getElementById("CurrGPGTextArea");


  document.addEventListener('DOMContentLoaded', function() {
    // // 🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
    // // The Firebase SDK is initialized and available here!
    //


    firebase.auth().onAuthStateChanged(user => {
      if (user) {
        firebaseuiAuthContainer.style.display = "none";
        userAuthContainer.style.display = "block";
        main.style.display = 'block';
        userNameContainer.innerText = user.email
        firestoreGet(CurrGPGTextAreaContainer, user.email)
      } else {
        firebaseuiAuthContainer.style.display = "block";
        userAuthContainer.style.display = "none";
        main.style.display = 'none';
      }
    });

    // firebase.database().ref('/path/to/ref').on('value', snapshot => { });
    // firebase.messaging().requestPermission().then(() => { });
    // firebase.storage().ref('/path/to/ref').getDownloadURL().then(() => { });
    //
    // // 🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥

    try {
      let app = firebase.app();
      let features = ['auth', 'database', 'messaging', 'storage', 'firestore'].filter(feature => typeof app[feature] === 'function');
      console.log(`Firebase SDK loaded with ${features.join(', ')}`);
    } catch (e) {
        console.error(e);
        console.error('Error loading the Firebase SDK, check the console.');
    }


// Initialize the FirebaseUI Widget using Firebase.
var ui = new firebaseui.auth.AuthUI(firebase.auth());

var uiConfig = {
callbacks: {
signInSuccessWithAuthResult: function(authResult, redirectUrl) {
  // User successfully signed in.
  // Return type determines whether we continue the redirect automatically
  // or whether we leave that to developer to handle.
  return true;
},
uiShown: function() {
  // The widget is rendered.
  // Hide the loader.
  document.getElementById('loader').style.display = 'none';
}
},
// Will use popup for IDP Providers sign-in flow instead of the default, redirect.
signInFlow: 'popup',
signInSuccessUrl: window.location.href,
  signInOptions: [
      {
        provider: firebase.auth.EmailAuthProvider.PROVIDER_ID,
          signInMethod: firebase.auth.EmailAuthProvider.EMAIL_LINK_SIGN_IN_METHOD
          },
    {
  provider: firebase.auth.GoogleAuthProvider.PROVIDER_ID,
  scopes: [],
  customParameters: {
    // Forces account selection even when one account
    // is available.
    prompt: 'select_account'
  }
},],
    };
ui.start('#firebaseui-auth-container', uiConfig)


});


function firestoreGet(destContainer, email) {
    console.log("firestore single query", email)
    db.collection("gmail.com").doc(email).collection("pub").doc("default")
        .get().then(function(doc) {
            if (doc.exists) {
                destContainer.innerText = window.atob(doc.data().data);
            } else {
                // doc.data() will be undefined in this case
                destContainer.innerText = "Key doesn't exist";
            }
        }).catch(function(error) {
            console.log("Error getting document:", error);
            destContainer.innerText = "Unexpected error";

        });
}

function firestorePut(data) {
    // Add a new document in collection "cities"
    var currUser = firebase.auth().currentUser
    db.collection("gmail.com").doc(currUser.email).collection("pub").doc("default").set({
        data: window.btoa(data),
    })
    .then(function() {
        console.log("Document successfully written!");
    })
    .catch(function(error) {
        console.error("Error writing document: ", error);
    });
}

firebase.analytics();
var db = firebase.firestore();

