/* 
   Proiect Pachete Software - Analiza Datelor Financiare CD Projekt Red (SAS)
   Sursa date: Data_Source/cdpr_cleaned.csv
   Autor: [Nume Student]
*/

proc import datafile="g:\salvat-pc-vechi\facultate\Year3\S2\PS\repo\Proiect-Pachete-Software\Data_Source\cdpr_cleaned.csv"
    out=work.cdpr_data
    dbms=csv
    replace;
    getnames=yes;
run;

proc format;
    value profit_cat
        low - 0 = "Pierdere"
        0 - 200000 = "Profit Moderat"
        200000 - high = "Profit Ridicat";
        
    value deceniu_fmt
        2010 - 2019 = "Deceniul 2010s"
        2020 - high = "Deceniul 2020s";
run;

data work.cdpr_refined;
    set work.cdpr_data;
    
    Profit_Margin = ROUND((NetProfit / Revenue) * 100, 0.01);
    
    if Profit_Margin > 30 then Performanta = "Excelenta";
    else if Profit_Margin > 0 then Performanta = "Stabila  ";
    else Performanta = "Critica  ";

    array regiuni[*] North_America_Pct Europe_Pct Asia_Pct Poland_Pct;
    Suma_Ponderi_Regionale = 0;
    do i = 1 to dim(regiuni);
        if not missing(regiuni[i]) then Suma_Ponderi_Regionale = Suma_Ponderi_Regionale + regiuni[i];
    end;
    drop i;

    if not missing(Year);
run;

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

proc sort data=work.cdpr_refined; by Year; run;
proc sort data=work.meta_evenimente; by Year; run;

data work.cdpr_final;
    merge work.cdpr_refined(in=a) work.meta_evenimente(in=b);
    by Year;
    if a; 
run;

title "Raport Financiar CD Projekt Red (Selectie)";
proc print data=work.cdpr_final noobs;
    var Year Revenue NetProfit Profit_Margin Performanta Eveniment_Major;
    format NetProfit profit_cat.;
run;

title "Distributia Performantei in raport cu Evenimentele Majore";
proc freq data=work.cdpr_final;
    tables Performanta * Eveniment_Major / nocol norow nopercent;
run;

title "Indicatori Statistici: Venituri, Profit si Cheltuieli Marketing";
proc means data=work.cdpr_final mean min max std;
    var Revenue NetProfit MarketingCosts;
    class Year;
    format Year deceniu_fmt.;
run;

title "Corelatia dintre Venituri, Cheltuieli Marketing si Profit Net";
proc corr data=work.cdpr_final;
    var MarketingCosts Assets;
    with Revenue NetProfit;
run;

title "Evolutia in timp a Veniturilor si Profitului Operational";
proc sgplot data=work.cdpr_final;
    series x=Year y=Revenue / lineattrs=(color=blue thickness=2) legendlabel="Venituri (PLN)";
    series x=Year y=OperatingProfit / lineattrs=(color=green thickness=2) legendlabel="Profit Operational (PLN)";
    xaxis label="Anul Raportarii";
    yaxis label="Valoare";
run;

data work.ml_data;
    set work.cdpr_final;
    if Performanta = "Excelenta" then Este_Excelent = 1;
    else Este_Excelent = 0;
run;

title "Model Machine Learning: Predictia Anilor Excelenti (Regresie Logistica)";
proc logistic data=work.ml_data descending;
    model Este_Excelent = MarketingCosts Assets;
    score data=work.ml_data out=work.ml_predictions;
run;

title "Predictii Model (Date Istorice - Selectie)";
proc print data=work.ml_predictions(obs=10);
    var Year Este_Excelent P_1;
run;

data work.date_viitoare;
    input Year MarketingCosts Assets;
    datalines;
2026 250000 3800000
;
run;

data work.date_complete;
    set work.ml_data work.date_viitoare;
run;

title "1. Predictia sumei exacte a Veniturilor pentru 2026 (PROC REG)";
proc reg data=work.date_complete;
    model Revenue = MarketingCosts Assets;
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

title;
