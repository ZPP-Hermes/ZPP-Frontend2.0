/* parametry skryptu (18)
 * 1 - liczba wygenerowanych zestawów ocen (plus wyborów seminariów)
 * 2 - offset (żeby pk studentów zaczynały się dalej)
 * 3-9 - procentowy średni rozkład ocen (od 2 do 5!), ma się sumować do 100
 * 10-16 - procentowy odchył od tego rozkładu (dla grupy docelowej i pobliskich),
 * ma się sumować do 0 (ujemne np. dla słabych ocen) najlepiej 
 * jakby moduły poszczególnych procentów nie przekraczały 9/11 odpowiedniego średniego
 * 17 - średni procent wybranych obieraków
 * 18 - odchył tego wyboru (żeby grupa docelowa była częściej wybierana)
 * */



#include <stdio.h>
#include <stdlib.h>
	char nazwyobow[30][60] = {"Języki i narzędzia programowania 1", "Języki i narzędzia programowania 2", "Języki i narzędzia programowania 3", "Aplikacje WWW",
		"Indywidualny projekt programistyczny", "Inżynieria oprogramowania", "Systemy operacyjne", "Sieci komputerowe", "Bezpieczeństwo systemów komputerowych", 
		"Języki i paradygmaty programowania", "Programowanie obiektowe", "Bazy Danych", "Wstęp do programowania", "Architektura komputerów i sieci",
		"Problemy społeczne i zawodowe informatyki", "Algorytmy i struktury danych", "Języki, automaty i obliczenia", "Semantyka i weryfikacja programów", "Podstawy matematyki",
		"Matematyka dyskretna", "Metody numetyczne", "Analiza matematyczna dla informatyków 1", "Analiza matematyczna dla informatyków 2", "Raczhunek prawdopodobieństwa i statystyka",
		 "Geometria z algebrą liniową", "Rachunek prawdopodobieństwa 1", "Statystyka 1", "Algebra 1", "Równania różniczkowe zwyczajne", "Topologia 1"};
	char nazwyobier[20][60] = {"Zaawansowane systemy operacyjne", "Programowanie mikrokontrolerów", "Kompresja danych", "Przetwarzanie dużych danych",
		"Programowanie w logice", "Wstęp do biologii obliczeniowej", "Zaawansowane bazy danych", "Systemy uczące się", "Sztuczna inteligencja i systemy doradcze", "Data mining", "Algorytmika",
		"Algorytmy tekstowe", "Weryfikacja wspomagana komputerowo", "Wnioskowanie w serwisach i systemach informatycznych", "Teoria informacji", "Kryptografia",
		"Matematyka obliczeniowa 2", "Statystyka 2", "Rachunek prawdopodobieństwa 2", "Optymalizacja 1"};
	char nazwysem[10][60] = {"Systemy rozproszone", "Języki programowania", "Zagadnienia programowania obiektowego", "Wybrane aspekty inżynierii oprogramowania",
		"Analiza, wizualizacja i optymalizacja oprogramowania", "Innowacyjne zastosowania informatyki", "Molekularna biologia obliczeniowa", "Metody numeryczne",
		"Algorytmika", "Matematyka w informatyce"};
	char urlobow[30][20] = {"1000-223bJNP1", "1000-224bJNP2", "1000-225bJNP3", "1000-214bWWW", "1000-222bIPP", "1000-214bIOP", "1000-213bSOP", "1000-214bSIK", "1000-215bBSK",
		  "1000-216bJPP", "1000-212bPO", "1000-213bBAD", "1000-211bWPI", "1000-212bAKS", "1000-214bPSZ", "1000-213bASD", "1000-214bJAO", "1000-215bSWP", "1000-211bPM","1000-215bMNU",
		 "1000-212bMD", "1000-211bAM1", "1000-212bAM2", "1000-213bRPS", "1000-211bGAL", "1000-114bRP1a", "1000-115ST1a", "1000-113bAG1a", "1000-114bRRZa", "1000-113bTP1a"};
	char urlobier[20][20] = {"1000-2N09ZSO", "1000-2M08PMK", "1000-2N09KDW", "1000-2M13PDD", "1000-2N00PLO", "1000-2N03BO", "1000-2N09ZBD", "1000-2N09SUS", "1000-2N00SID",
		"1000-2M03DM", "1000-2N00ALG", "1000-2N09ALT", "1000-2N09WWK", "1000-2N09WSS", "1000-2N03TI", "1000-2M12KI1", "1000-135MO2", "1000-135ST2", "1000-135RP2", "1000-134OP1"};
	char urlsem[10][20] = {"1000-2D97SR", "1000-2D13JP", "1000-2D03PO", "1000-2D97IO", "1000-2D11WSI", "1000-2D10IZI", "1000-5D97MB", "1000-1L09MN", "1000-2D97AL", "1000-5D96MI"}; 
	int hardness[60] = {1,-4,-4,0,1,0,3,3,2,3,1,-2,0,-5,-4,0,-2,0,-2,-1,1,-1,-1,0,1,1,1,2,3,2,5,4,2,2,1,1,1,2,-1,1,2,1,-1,1,1,0,3,3,2,-1,0,0,0,0,0,0,0,0,0,0};
	int marks[7][60];
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
		return 1;
	}else{
		return 0;
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
	int i,j,k,n,r,off;
	if(argc!=19){
		fprintf(stderr, "zła liczba argumentów\n");
		return;
	}
	n=atoi(argv[1]);
	off=atoi(argv[2]);
	/*wczytanie parametrów i sprawdzenie warunków*/
	procenty[0]=atoi(argv[3]);
	for(i=1;i<7;++i){
		procenty[i]=procenty[i-1]+atoi(argv[i+3]);
	}
	if(procenty[6]!=100){
		fprintf(stderr, "procenty powinny się sumować do 100\n");
		return;
	}
	odchyly[0]=atoi(argv[10]);
	for(i=1;i<7;++i){
		odchyly[i]=odchyly[i-1]+atoi(argv[i+10]);
	}
	if(odchyly[6]!=0){
		fprintf(stderr, "odchyły powinny się sumować do 0\n");
		return;
	}
	wybieralnosc=atoi(argv[17]);
	wyb_odch=atoi(argv[18]);
	for(i=0;i<6;++i){
		for(j=0;j<60;++j){
			marks[i][j]=0;
		}
	}
	//TODO sprawdzić nie wychodzenie poza zakres procentów (a nawet 9/11)
	/*generowanie ocen*/
	srand(time(NULL));
	printf("[");
	for(i=0;i<60;++i){
		printf("{\"model\":\"app.course\",\"pk\" : %d, \"fields\": {\"name\":\"\", \"type\": \"OBOW\",\"url\":\"\","
		"\"mark4\":0,\"mark6\":0,\"mark7\":0,\"mark8\":0,\"mark9\":0,\"mark10\":0,\"mark11\":0}},\n",i+1);
	}
	for(i=off;i<n+off;++i){
		printf("{\"model\":\"app.student\",\"pk\" : %d, \"fields\": {\"usos_id\":\"%d\"}},\n",i+1,i+1);
		k=rand()%10;
		for(j=0;j<30;++j){
			printf("{\"model\":\"app.mark\", \"fields\": {\"student\":%d, \"course\":%d, \"mark\": \"%d\"}},\n",i+1,j+1,rank(k,j/3,j));
		}
		for(j=0;j<20;++j){
			if(choose(k,j/2)!=0){
				printf("{\"model\":\"app.mark\", \"fields\": {\"student\":%d, \"course\":%d, \"mark\": \"%d\"}},\n",i+1,j+31,rank(k,j/2,j+30));
			}
		}
		printf("{\"model\":\"app.mark\", \"fields\": {\"student\":%d, \"course\":%d, \"mark\": \"%d\"}},\n",i+1,k+51,rank(k,k,k+50));
	}
	for(i=0;i<30;++i){
		printf("{\"model\":\"app.course\",\"pk\" : %d, \"fields\": {\"name\":\"%s\", \"type\": \"OBOW\",\"url\":\"%s\","
		"\"mark4\":%d,\"mark6\":%d,\"mark7\":%d,\"mark8\":%d,\"mark9\":%d,\"mark10\":%d,\"mark11\":%d}},\n",
		i+1,nazwyobow[i],urlobow[i],marks[0][i],marks[1][i],marks[2][i],marks[3][i],marks[4][i],marks[5][i],marks[6][i]);
	}
	for(i=0;i<20;++i){
		printf("{\"model\":\"app.course\",\"pk\" : %d, \"fields\": {\"name\":\"%s\", \"type\": \"OBIER\",\"url\":\"%s\","
		"\"mark4\":%d,\"mark6\":%d,\"mark7\":%d,\"mark8\":%d,\"mark9\":%d,\"mark10\":%d,\"mark11\":%d}},\n",
		i+31,nazwyobier[i],urlobier[i],marks[0][i+30],marks[1][i+30],marks[2][i+30],marks[3][i+30],marks[4][i+30],marks[5][i+30],marks[6][i+30]);
	}
	for(i=0;i<10;++i){
		printf("{\"model\":\"app.course\",\"pk\" : %d, \"fields\": {\"name\":\"%s\", \"type\": \"SEM\",\"url\":\"%s\","
		"\"mark4\":%d,\"mark6\":%d,\"mark7\":%d,\"mark8\":%d,\"mark9\":%d,\"mark10\":%d,\"mark11\":%d}},\n",
		i+51,nazwysem[i],urlsem[i],marks[0][i+50],marks[1][i+50],marks[2][i+50],marks[3][i+50],marks[4][i+50],marks[5][i+50],marks[6][i+50]);
	}
	printf("{\"model\":\"app.student\",\"pk\" : %d, \"fields\": {\"usos_id\":\"%d\"}}\n",n+1,n+1);
	printf("]");

}
