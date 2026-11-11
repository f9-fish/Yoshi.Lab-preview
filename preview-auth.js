// Preview-only auth: no profile, learning record, XP, or last-access reads/writes.
import {initializeApp} from 'https://www.gstatic.com/firebasejs/13.1.0/firebase-app.js';
import {getAuth,GoogleAuthProvider,signInWithPopup,onAuthStateChanged,signOut,browserSessionPersistence,setPersistence} from 'https://www.gstatic.com/firebasejs/13.1.0/firebase-auth.js';
import {getDatabase,ref,get} from 'https://www.gstatic.com/firebasejs/13.1.0/firebase-database.js';
const app=initializeApp({apiKey:'AIzaSyDhm9zeUsgvF6_lbwcRj57VWXzYPA3LEzM',authDomain:'yoshi-lab-db3eb.firebaseapp.com',databaseURL:'https://yoshi-lab-db3eb-default-rtdb.firebaseio.com',projectId:'yoshi-lab-db3eb',appId:'1:543561154900:web:b9ba898d1d44a385f848c1'},'yoshilab-studio-preview');
const auth=getAuth(app),db=getDatabase(app),listeners=new Set(),provider=new GoogleAuthProvider();
provider.setCustomParameters({prompt:'select_account'});
let current=null,ready=false;
const persistence=setPersistence(auth,browserSessionPersistence);
window.YoshiAccount={
 get user(){return current},
 subscribe(fn){listeners.add(fn);if(ready)fn(current);return()=>listeners.delete(fn)},
 async login(){await persistence;return signInWithPopup(auth,provider)},
 async logout(){return signOut(auth)},
 async getToken(){if(!current)throw Error('Googleログインが必要です');return current.getIdToken()},
 async isTeacher(){const user=current;if(!user)return false;const claims=await user.getIdTokenResult();if(!user.emailVerified||claims.signInProvider!=='google.com')return false;const snap=await get(ref(db,'teacherUids/'+user.uid));return current===user&&snap.val()===true}
};
onAuthStateChanged(auth,user=>{current=user?.emailVerified?user:null;ready=true;for(const fn of listeners)fn(current)});
