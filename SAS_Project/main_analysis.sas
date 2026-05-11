/* 
   Proiect Pachete Software - Analiza Datelor Financiare CD Projekt Red (SAS)
   Sursa date: Data_Source/cdpr_cleaned.csv
   Autor: [Nume Student]
*/

/* -------------------------------------------------------------------------
   CERINTA 1: Crearea unui set de date SAS din fișiere externe
   SEMINAR: Seminarul 2 si SAS ML (PROC IMPORT)
   Explicatie: Importam datele financiare dintr-un fisier CSV extern intr-un 
   set de date SAS temporar numit 'cdpr_data'.
   ------------------------------------------------------------------------- */
proc import datafile="g:\salvat-pc-vechi\facultate\Year3\S2\PS\repo\Proiect-Pachete-Software\Data_Source\cdpr_cleaned.csv"
    out=work.cdpr_data
    dbms=csv
    replace;
    getnames=yes;
run;

/* -------------------------------------------------------------------------
   CERINTA 2: Crearea și folosirea de formate definite de utilizator
   SEMINAR: Seminarul 2 (Formate si etichete)
   Explicatie: Definim formate personalizate pentru a categorisi nivelul de 
   profit (profit_cat) si deceniul in care ne aflam (deceniu_fmt).
   ------------------------------------------------------------------------- */
proc format;
    value profit_cat
        low - 0 = "Pierdere"
        0 - 200000 = "Profit Moderat"
        200000 - high = "Profit Ridicat";
        
    value deceniu_fmt
        2010 - 2019 = "Deceniul 2010s"
        2020 - high = "Deceniul 2020s";
run;

/* -------------------------------------------------------------------------
   CERINTA 3, 4, 5, 7: Procesare iterativa si conditionala, creare subseturi, 
                       functii SAS, utilizare masive (arrays)
   SEMINAR: Seminarul 2 (Instructiunea IF), Seminarul 3 (Bucla DO, ARRAY, Functii)
   Explicatie: Intr-un pas DATA, parcurgem setul de date si aplicam transformari.
   ------------------------------------------------------------------------- */
data work.cdpr_refined;
    set work.cdpr_data;
    
    /* CERINTA 5 (Functii SAS): Folosim functii matematice pentru calcule.
       Seminar 3 (Functii SAS) */
    Profit_Margin = ROUND((NetProfit / Revenue) * 100, 0.01);
    
    /* CERINTA 3 (Procesare conditionala): IF-THEN-ELSE
       Seminar 2 (Instructiunea IF) */
    if Profit_Margin > 30 then Performanta = "Excelenta";
    else if Profit_Margin > 0 then Performanta = "Stabila  ";
    else Performanta = "Critica  ";

    /* CERINTA 7 (Utilizarea de masive/arrays) si CERINTA 3 (Procesare iterativa)
       Seminar 3 (Masive si Bucla DO)
       Aici folosim un ARRAY pentru a aduna procentele de vanzari pe regiuni 
       pentru a ne asigura ca suma lor e apropiata de 1 (100%). */
    array regiuni[*] North_America_Pct Europe_Pct Asia_Pct Poland_Pct;
    Suma_Ponderi_Regionale = 0;
    do i = 1 to dim(regiuni);
        /* Daca valoarea nu lipseste, o adaugam la suma */
        if not missing(regiuni[i]) then Suma_Ponderi_Regionale = Suma_Ponderi_Regionale + regiuni[i];
    end;
    drop i; /* Stergem variabila contor din setul final */

    /* CERINTA 4 (Crearea de subseturi de date)
       Seminar 2 (Selectarea observatiilor)
       Pastram doar anii in care datele nu au erori majore in dataset (ex: anul valid) */
    if not missing(Year);
run;

/* -------------------------------------------------------------------------
   CERINTA 6: Combinarea seturilor de date prin proceduri specifice SAS și SQL
   SEMINAR: Seminarul 3 (Proceduri specifice SQL si MERGE)
   Explicatie: Cream un set de date aditional folosind PROC SQL care contine
   informatii despre lansarile majore, apoi facem MERGE (Left Join).
   ------------------------------------------------------------------------- */

/* Crearea unui subset aditional prin SQL */
proc sql;
    create table work.meta_evenimente as
    select Year, 
           case when Year = 2020 then "Lansare Cyberpunk 2077"
                when Year = 2021 then "Declin/Refacere Post-Lansare"
                when Year = 2022 then "Revenire (Anime Edgerunners)"
                when Year = 2023 then "Lansare DLC (Phantom Liberty)"
                else "An Intermediar"
           end as Eveniment_Major
    from work.cdpr_data;
quit;

/* Sortam inainte de MERGE, obligatoriu conform Seminarului 3 */
proc sort data=work.cdpr_refined; by Year; run;
proc sort data=work.meta_evenimente; by Year; run;

/* Realizam fuziunea bazata pe o corespondenta unu-la-unu folosind MERGE */
data work.cdpr_final;
    merge work.cdpr_refined(in=a) work.meta_evenimente(in=b);
    by Year;
    /* Pastram doar datele care exista in setul de date principal (Left Join logic) */
    if a; 
run;

/* -------------------------------------------------------------------------
   CERINTA 8: Utilizarea de proceduri pentru raportare
   SEMINAR: Seminarul 4 (Procedura PRINT si FREQ)
   Explicatie: Generam rapoarte detaliate si de frecventa.
   ------------------------------------------------------------------------- */
title "Raport Financiar CD Projekt Red (Selectie)";
proc print data=work.cdpr_final noobs;
    var Year Revenue NetProfit Profit_Margin Performanta Eveniment_Major;
    /* Aplicam formatul definit la Cerinta 2 */
    format NetProfit profit_cat.;
run;

title "Distributia Performantei in raport cu Evenimentele Majore";
proc freq data=work.cdpr_final;
    tables Performanta * Eveniment_Major / nocol norow nopercent;
run;

/* -------------------------------------------------------------------------
   CERINTA 9: Folosirea de proceduri statistice
   SEMINAR: Seminarul 4 (Procedura MEANS si CORR)
   Explicatie: Analizam indicatori statistici si corelatiile dintre variabile.
   ------------------------------------------------------------------------- */
title "Indicatori Statistici: Venituri, Profit si Cheltuieli Marketing";
proc means data=work.cdpr_final mean min max std;
    var Revenue NetProfit MarketingCosts;
    /* Analizam datele grupate pe decenii folosind formatul creat */
    class Year;
    format Year deceniu_fmt.;
run;

title "Corelatia dintre Venituri, Cheltuieli Marketing si Profit Net";
proc corr data=work.cdpr_final;
    var MarketingCosts Assets;
    with Revenue NetProfit;
run;

/* -------------------------------------------------------------------------
   CERINTA 10: Generarea de grafice
   SEMINAR: Seminarul 4 (Procedura GPLOT/GCHART, noi folosim SGPLOT ca varianta moderna)
   Explicatie: Grafic de tip serie temporala pentru a vedea evolutia financiara.
   ------------------------------------------------------------------------- */
title "Evolutia in timp a Veniturilor si Profitului Operational";
proc sgplot data=work.cdpr_final;
    series x=Year y=Revenue / lineattrs=(color=blue thickness=2) legendlabel="Venituri (PLN)";
    series x=Year y=OperatingProfit / lineattrs=(color=green thickness=2) legendlabel="Profit Operational (PLN)";
    xaxis label="Anul Raportarii";
    yaxis label="Valoare";
run;

/* -------------------------------------------------------------------------
   CERINTA 11: SAS ML (Machine Learning)
   SEMINAR: SAS ML (Regresia Logistica - PROC LOGISTIC)
   Explicatie: Construim un model de regresie logistica pentru a prezice daca
   un an va avea performanta "Excelenta" pe baza costurilor de marketing si activelor.
   ------------------------------------------------------------------------- */
/* Pregatim datele: transformam clasa in variabila binara (1/0) */
data work.ml_data;
    set work.cdpr_final;
    if Performanta = "Excelenta" then Este_Excelent = 1;
    else Este_Excelent = 0;
run;

title "Model Machine Learning: Predictia Anilor Excelenti (Regresie Logistica)";
/* Construirea modelului de regresie logistica, conform seminarului ML */
proc logistic data=work.ml_data descending;
    model Este_Excelent = MarketingCosts Assets;
    /* Salvam rezultatele predicite intr-un set de testare.
       Aici folosim acelasi dataset pentru simplitate in scop demonstrativ. */
    score data=work.ml_data out=work.ml_predictions;
run;

title "Predictii Model (Date Istorice - Selectie)";
proc print data=work.ml_predictions(obs=10);
    var Year Este_Excelent P_1;
run;

/* --- PREDICTIE PENTRU VIITOR --- */
/* Pentru a raspunde nevoii de business de a cunoaste sume exacte, vom 
   folosi atat Regresie Logistica (pentru probabilitatea de succes) 
   cat si Regresie Liniara (PROC REG din Seminarul 4) pentru a prezice
   suma exacta a Veniturilor (Revenue) pentru anul 2026. */

/* Cream setul de date pentru viitor cu scenariul de buget propus */
data work.date_viitoare;
    input Year MarketingCosts Assets;
    /* Lasam Revenue si Performanta goale, ele vor fi prezise */
    datalines;
2026 250000 3800000
;
run;

/* Imbinam datele viitoare cu cele istorice pentru a facilita predictia */
data work.date_complete;
    set work.ml_data work.date_viitoare;
run;

title "1. Predictia sumei exacte a Veniturilor pentru 2026 (PROC REG)";
proc reg data=work.date_complete;
    model Revenue = MarketingCosts Assets;
    /* Generam predictiile matematice si filtram sa afiseze doar anul 2026 */
    output out=work.rezultat_regresie(where=(Year=2026)) p=Venit_Estimat;
run;

proc print data=work.rezultat_regresie;
    var Year MarketingCosts Assets Venit_Estimat;
    format Venit_Estimat COMMA15.2;
run;

title "2. Predictia riscului/probabilitatii de a fi un an Excelent (PROC LOGISTIC)";
proc logistic data=work.ml_data descending;
    model Este_Excelent = MarketingCosts Assets;
    score data=work.date_viitoare out=work.predictie_logistic;
run;

proc print data=work.predictie_logistic;
    var Year MarketingCosts Assets P_1;
run;

/* Stergerea titlului final */
title;
