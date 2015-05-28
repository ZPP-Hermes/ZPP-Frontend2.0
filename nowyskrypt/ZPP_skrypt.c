/* parametry skryptu (17)
 * 1 - liczba wygenerowanych zestawów ocen (plus wyborów seminariów)
 * 2-8 - procentowy średni rozkład ocen (od 2 do 5!), ma się sumować do 100
 * 9-15 - procentowy odchył od tego rozkładu (dla grupy docelowej i pobliskich),
 * ma się sumować do 0 (ujemne np. dla słabych ocen) najlepiej 
 * jakby moduły poszczególnych procentów nie przekraczały 9/11 odpowiedniego średniego
 * 16 - średni procent wybranych obieraków
 * 17 - odchył tego wyboru (żeby grupa docelowa była częściej wybierana)
 * */



#include <stdio.h>
#include <stdlib.h>
	int marks[7][60];
	int hardness[51] = {1,-4,-4,0,1,0,3,3,2,3,1,-2,0,-5,-4,0,-2,0,-2,-1,1,-1,-1,0,1,1,1,2,3,2,5,4,2,2,1,1,1,2,-1,1,2,1,-1,1,1,0,3,3,2,-1,0,0,0,0,0,0,0,0,0,0};
	int ext[2][7]={{1,8,21,40,70,95,100},{60,82,92,97,99,100,100}};
	int wyrownanie[10]={45,37,31,27,25,25,27,31,37,45};
	int procenty[7], odchyly[7];
	int wybieralnosc,wyb_odch;

float modul(int k, int l){
	int m = (k<l?l-k:k-l);
	return 1.0-(10.0*m)/wyrownanie[l];
}

int choose(int k, int l){
	int r=rand()%100;
	if(r<wybieralnosc+wyb_odch*modul(k,l)){
		return 0;
	}else{
		return 1;
	}
}

int rank(int k, int l,int p){
	float m = modul(k,l);
	int r=rand()%100;
	int i,h,res;
	if(hardness[p]>=0){
		h=hardness[p];
		i=1;
	}else{
		h=-hardness[p];
		i=0;
	}
	if(10*r<(10-h)*(procenty[0]+m*odchyly[0])+h*(ext[i][0])){
		marks[0][p]++;
		return 4;
	}else if(10*r<(10-h)*(procenty[1]+m*odchyly[1])+h*(ext[i][1])){
		marks[1][p]++;
		return 6;
	}else if(10*r<(10-h)*(procenty[2]+m*odchyly[2])+h*(ext[i][2])){
		marks[2][p]++;
		return 7;
	}else if(10*r<(10-h)*(procenty[3]+m*odchyly[3])+h*(ext[i][3])){
		marks[3][p]++;
		return 8;
	}else if(10*r<(10-h)*(procenty[4]+m*odchyly[4])+h*(ext[i][4])){
		marks[4][p]++;
		return 9;
	}else if(10*r<(10-h)*(procenty[5]+m*odchyly[5])+h*(ext[i][5])){
		marks[5][p]++;
		return 10;
	}else{
		marks[6][p]++;
		return 11;
	}
}


void main(int argc, char *argv[]){
	int i,j,k,n,r;
	
	if(argc!=18){
		fprintf(stderr, "zła liczba argumentów\n");
		return;
	}
	n=atoi(argv[1]);
	/*wczytanie parametrów i sprawdzenie warunków*/
	procenty[0]=atoi(argv[2]);
	for(i=1;i<7;++i){
		procenty[i]=procenty[i-1]+atoi(argv[i+2]);
	}
	if(procenty[6]!=100){
		fprintf(stderr, "procenty powinny się sumować do 100\n");
		return;
	}
	odchyly[0]=atoi(argv[9]);
	for(i=1;i<7;++i){
		odchyly[i]=odchyly[i-1]+atoi(argv[i+9]);
	}
	if(odchyly[6]!=0){
		fprintf(stderr, "odchyły powinny się sumować do 0\n");
		return;
	}
	wybieralnosc=atoi(argv[16]);
	wyb_odch=atoi(argv[17]);
	//TODO sprawdzić nie wychodzenie poza zakres procentów (a nawet 9/11)
	/*generowanie ocen*/
	srand(time(NULL));
	for(i=0;i<n;++i){
		k=rand()%10;
		for(j=0;j<30;++j){
			printf("%d,",rank(k,j/3,j));
		}
		for(j=0;j<20;++j){
			printf("%d,",(choose(k,j/2)?rank(k,j/2,j+30):0));
		}
		printf("%d\n",k);
	}

}
