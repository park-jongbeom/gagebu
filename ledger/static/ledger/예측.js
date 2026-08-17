
axios.interceptors.request.use(설정 => {
    설정.headers["X-Token"] = "practice-token";
    return 설정;
});

const 항목칸 = document.getElementById("항목칸");
const 단추 = document.getElementById("물어보기");
const 로딩 = document.getElementById("로딩");
const 결과 = document.getElementById("결과");
const 그림칸 = document.getElementById("그림칸");
const 알아보기 = document.getElementById("알아보기");

단추.addEventListener("click", 물어본다);

async function 물어본다(){
    로딩.textContent = "불러오는 중입니다";
    결과.textContent = "";
    try{
    const 답 = await axios.post("/api/예측/",{항목:항목칸.value});
    결과.textContent = 답.data.분류 + " - 확신 "+ 답.data.확신;
    } catch (오류) {
        if(오류.response){            
        결과.textContent = "보낸 값을 확인해 주십시오";
        }else{            
        결과.textContent = "서버에 닿지 못했습니다";
        }
    } finally {
        로딩.textContent = "";
    }
}

알아보기.addEventListener("click", async () =>{
    const 짐 = new FormData();
    짐.append("그림", 그림칸.files[0]);
    const 답 = await axios.post("/api/그림/", 짐);
    결과.textContent = 답.data.파일 + " -> " + 답.data.숫자;
});