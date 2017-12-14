function ready_Select(){
    var table = document.getElementById('result_table');
    var tr = table.getElementsByTagName("tr");
    var td = new Array();
    var cnt = 0;
    var kind1 = table.getElementsByClassName('kind1')
    var good_list = new Array();
    var bad_list = new Array();
    var manual_list = new Array();
    var impossible = new Array();
    var etc_list = new Array();
    var result_list = new Array();
    for (area = 0; area < tr.length; area++){
        if (tr[area].getElementsByTagName('td').length == 5){       
            var td = tr[area].getElementsByTagName('td')[4].textContent;
        }
        else if(tr[area].getElementsByTagName('td').length == 4){
            var td = tr[area].getElementsByTagName('td')[3].textContent;
        }
        
        if(td =='양호'){
            good_list[good_list.length] = tr[area];
        }
        else if (td =='취약'){
            bad_list[bad_list.length] = tr[area];
        }
        else if (td =='수동'){
            manual_list[manual_list.length] = tr[area];
        }
        else if (td =='측정불가'){
            impossible[impossible.length] = tr[area];
        }
        else if (td =='비 정 상'){
            etc_list[etc_list.length] = tr[area];
        }
    }
    result_list[0] = good_list; // 양호
    result_list[1] = bad_list; // 취약
    result_list[2] = etc_list; // 비정상
    result_list[3] = manual_list; // 수동
    result_list[4] = impossible; // 측정불가
    return result_list
}


// ---------------- Filtering Start ----------------

function filtering(text){
    var str = text; // 현재 Select된 텍스트 값 (양호, 취약, 비정상, 측정불가, Show All)
    var good = ready_Select()[0]; // 양호
    var bad = ready_Select()[1];  // 취약
    var etc = ready_Select()[2];  // 비정상
    var manual = ready_Select()[3]; // 수동
    var impossible = ready_Select()[4]; // 측정불가

    filter_ShowAll();
    if (str == '양호'){
        
        var management = kind_True(good); // rowspan의 갯수를 셈
        
        for (x=0; x < good.length; x++){
            good[x].style.display = "";
        }
        for (y=0; y < bad.length; y++){
            bad[y].style.display = "none";
        }
        for (z=0; z < etc.length; z++){
            etc[z].style.display = "none";
        }
        for (a=0; a < manual.length; a++){
            manual[a].style.display = "none";
        }
        for (b=0; b < impossible.length; b++){
            impossible[b].style.display = "none";
        }
        filter_display(management,str);
    }
    else if (str == '취약'){
        var management = kind_True(bad); // rowspan의 갯수를 셈
        
        for (x=0; x < good.length; x++){
            good[x].style.display = "none";
        }
        for (y=0; y < bad.length; y++){
            bad[y].style.display = "";
//            rowspan_Condition(management,1);
        }
        for (z=0; z < etc.length; z++){
            etc[z].style.display = "none";
        }
        for (a=0; a < manual.length; a++){
            manual[a].style.display ="none";
        }
        for (b=0; b < impossible.length; b++){
            impossible[b].style.display = "none";
        }
        filter_display(management,str);
    }
    else if (str =='비 정 상'){
        
        var management = kind_True(etc); // rowspan의 갯수를 셈
        
        for (x=0; x < good.length; x++){
            good[x].style.display = "none";
        }
        for (y=0; y < bad.length; y++){
            bad[y].style.display = "none";
        }
        for (z=0; z < etc.length; z++){
            etc[z].style.display = "";
//            rowspan_Condition(management,2);
        }
        for (a=0; a < manual.length; a++){
            manual[a].style.display ="none";
        }
        for (b=0; b < impossible.length; b++){
            impossible[b].style.display = "none";
        }
        filter_display(management,str);
    }
    else if (str =='수동'){
        
        var management = kind_True(manual); // rowspan의 갯수를 셈
        
        for (x=0; x<good.length; x++){
            good[x].style.display = "none";
        }
        for (y=0; y < bad.length; y++){
            bad[y].style.display = "none";
        }
        for (z=0; z < etc.length; z++){
            etc[z].style.display = "none";
        }
        for (a=0; a < manual.length; a++){
            manual[a].style.display ="";
        }
        for (b=0; b < impossible.length; b++){
            impossible[b].style.display = "none";
        }
        filter_display(management,str);
    }
    else if (str =='측정불가'){
        
        var management = kind_True(impossible); // rowspan의 갯수를 셈
        
        for (x=0; x<good.length; x++){
            good[x].style.display = "none";
        }
        for (y=0; y < bad.length; y++){
            bad[y].style.display = "none";
        }
        for (z=0; z < etc.length; z++){
            etc[z].style.display = "none";
        }
        for (a=0; a < manual.length; a++){
            manual[a].style.display ="none";
        }
        for (b=0; b < impossible.length; b++){
            impossible[b].style.display = "";
        }
        filter_display(management,str);
    }
    else if (str == 'show'){
        filter_ShowAll();
        for (x=0; x < good.length; x++){
            good[x].style.display = ""; // 양호 모두 보이기
        }
        for (y=0; y < bad.length; y++){
            bad[y].style.display = ""; // 취약 모두 보이기
        }
        for (z=0; z < etc.length; z++){
            etc[z].style.display = ""; // 비정상 모두 보이기
        }
        for (a=0; a < manual.length; a++){
            manual[a].style.display =""; // 수동 모두 보이기
        }
        for (b=0; b < impossible.length; b++){
            impossible[b].style.display = ""; // 측정불가 모두 보이기
        }
    }
}

// ---------------- Filtering End ----------------


// -------------- Rowspan Check Start --------------
function kind_True(kind){
    var flag = new Array(0,0,0,0,0,0);
    var flag2 = new Array();
    var cnt1 =new Array(), cnt2=new Array(), cnt3=new Array(), cnt4=new Array(), cnt5=new Array(), cnt6=new Array();
    var cout1=0,cout2=0,cout3=0,cout4=0,cout5=0,cout6=0;
    
    for (x=0; x < kind.length; x++){
        var f1 = kind[x].getElementsByClassName('wcode')[0].textContent; // W code Parser
        f1 = f1.replace("W-",""); 
        f1 = parseInt(f1); // W code number
        if (f1 > 0 && f1 < 19){     // 계정 관리
            cout1 +=1;
            flag[0] = cout1;
            cnt1[cnt1.length] = f1;
        }
        else if(f1 > 18 && f1 < 55){    // 서비스 관리
            cout2+=1;
            flag[1] = cout2;
            cnt2[cnt2.length] = f1;
        }
        else if (f1 > 54 && f1 < 58){       // 패치 관리
            cout3+=1;
            flag[2] = cout3;
            cnt3[cnt3.length] = f1;
        }
        else if (f1 > 57 && f1 < 62){       // 로그 관리
            cout4+=1;
            flag[3] = cout4;
            cnt4[cnt4.length] = f1;
        }
        else if(f1 > 61 && f1 < 82){        // 보안 관리
            cout5+=1;
            flag[4] = cout5;
            cnt5[cnt5.length] = f1;
        }
        else if(f1 == 82){          // DB 관리
            cout6+=1;
            flag[5] = cout6;
            cnt6[cnt6.length] = f1;
        }
    }
    flag2[0] = cnt1;
    flag2[1] = cnt2;
    flag2[2] = cnt3;
    flag2[3] = cnt4;
    flag2[4] = cnt5;
    flag2[5] = cnt6;
    var result = new Array(flag,flag2);
    return result;
}
// -------------- Rowspan Check End --------------


function filter_display(manage,str){
    for (i=0; i < manage[0].length; i++){
        var cnt = i+1;
        var service = 'service' + cnt;
        var division = 'kind' + cnt;
        var status = document.getElementById(service).getElementsByTagName('td')[4].textContent;
        var service_id = document.getElementById(service)
        var service_code = service_id.getElementsByTagName('td')[1].textContent.replace("W-","");
        var flag = false;
        var span = "";
        service_code = parseInt(service_code);

        if (manage[1][i][0] != service_code){
//            for (s=0; s<manage[1][i].length; s++){
            add = manage[0][i];
            span = span+add;
            i_num = i+1;
            kinds = "new_kind" +i_num;
            new_manage = service_id.querySelector('td').textContent;
            var tmp = "W-" + manage[1][i];
            numb = i+1;
            try{
                document.getElementsByTagName('tr')[manage[1][i][0]+1].insertCell(0);
            }
            catch (exception){
                continue;
            }
            document.getElementsByTagName('tr')[manage[1][i][0]+1].querySelector('td').innerHTML=new_manage;
            document.getElementsByTagName('tr')[manage[1][i][0]+1].querySelector('td').className='new_kind'+numb;
            document.getElementsByClassName(kinds)[0].rowSpan = span; // new_kind를 변수로 
            document.getElementById(service).style.display="none";
            flag=true;
        }
        else{
            add = manage[0][i];
            span = span+add;
            document.getElementsByClassName(division)[0].rowSpan = span;
            document.getElementById(service).style.display="";
        }

        
        
        
        
        
        if (manage[0][i] > 0){
            if(str == status){
               continue;
            }
            else{
                for (num=0; num <5; num++){
                    var td = document.getElementById(service).getElementsByTagName('td')[num];
                    if (num == 0 && flag==false){
                        td.style.display= '';
                    }
                    else{
                        td.style.display = 'none';
                        
                    }
                }
            }
        }
        else{
            document.getElementById(service).style.display="none";
            continue;
        }
    }
}





function filter_ShowAll(){
    for (i=0; i < 6; i++){
        var cnt = i+1;
        var service = 'service' + cnt;
        var division = 'kind' + cnt;
        var new_division = 'new_kind' + cnt;
        if (division == 'kind1'){
            leng = 18;
            document.getElementById(service).getElementsByClassName(division)[0].rowSpan = leng;   
            filter_ShowSub(service);
            newKind_remove(leng,new_division);
        }
        else if(division == 'kind2'){
            leng = 36;
            document.getElementById(service).getElementsByClassName(division)[0].rowSpan = leng;
            filter_ShowSub(service);
            newKind_remove(leng,new_division);
        }
        else if(division == 'kind3'){
            leng = 3;
            document.getElementById(service).getElementsByClassName(division)[0].rowSpan = leng;
            filter_ShowSub(service);
            newKind_remove(leng,new_division);
        }
        else if(division == 'kind4'){
            leng = 4;
            document.getElementById(service).getElementsByClassName(division)[0].rowSpan = leng;
            filter_ShowSub(service);
            newKind_remove(leng,new_division);
        }
        else if(division == 'kind5'){
            leng = 20;
            document.getElementById(service).getElementsByClassName(division)[0].rowSpan = leng; 
            filter_ShowSub(service);
            newKind_remove(leng,new_division);
        }
        else if (division == 'kind6'){
            leng = 1;
            document.getElementById(service).getElementsByClassName(division)[0].rowSpan = leng;
            filter_ShowSub(service);
            newKind_remove(leng,new_division);
        }
        
    }
}

function filter_ShowSub(service){
    for (num=0; num <5; num++){
        document.getElementById(service).getElementsByTagName('td')[num].style.display = '';
        }
}

function newKind_remove(leng,division){
    for (num=0; num<leng; num++){
        child = document.getElementsByClassName(division);
        try{
            pn = child[0].parentNode;
            pn.removeChild(document.getElementsByClassName(division)[0]);
        }
        catch (exception){
            continue;
        }
    }
}