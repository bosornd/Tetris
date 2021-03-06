# Tetris

* 오류 관련 사항  
(제 컴퓨터와 지인 컴퓨터에선 오류가 없었으나 일부 사람들에게 오류가 발생한다고 하니 다음 사항들을 확인해주세요.)  
1. Images 폴더와 마찬가지로 Sounds 폴더를 다운로드 받았는지 확인해주세요.
2. 거기에 'combo1.wav', 'fdrop.wav', 'game_clear.wav' 등 13개의 음원이 들어있는지 확인해주세요.
3. python 3.8을 사용중인지 확인해주세요.
4. bangtal 패키지가 최신버전 (0.3.1)인지 확인해주세요.
5. 위 방법을 전부 확인했는데 Type error: playSound() missing 1 required positional argument :'loop' 에러가 여전히 나타나나요?  
Tetris.py (코드) 에 모든 'play()'를 'play(False)' 로 바꾼 후 실행해보세요.  
이 오류가 아니라면, e-class 리뷰 코멘트에 오류내용을 알려주세요.  

---

  
![블록](https://user-images.githubusercontent.com/63161899/96385307-0208d300-11ce-11eb-902c-6b349ae60143.png)


반복해서 나오는 4개의 사각형을 조합한 테트로미노 7종류를 쌓는 게임입니다.

![설명6](https://user-images.githubusercontent.com/63161899/96385248-a2aac300-11cd-11eb-8b3f-603168da9168.PNG)

맨 위에서 나와 주기적으로 밑으로 낙하하는 블록이 현재블록입니다.  
그 밑에 회색 블록은 현재 블록이 떨어지는 예상 위치이고, 게임판 좌우에 각각 보관함(HOLD)와 다음번블록(NEXT)가 있습니다.

![설명5](https://user-images.githubusercontent.com/63161899/96385246-a2aac300-11cd-11eb-91a5-9358919179f4.PNG)

현재 블록은 시계/반시계 방향으로 돌리거나, 한칸 옆으로 움직이거나(위로 다시 올릴수는 없습니다.), 제일 아래로 내릴 수 있습니다.  
블록이 완전히 낙하하게되면 다음 블록이 나오고, 그 전에 저장해놓은 블록과 현재블록을 맞바꿀 수 있습니다.

---

블록을 각각의 줄이 꽉 차도록 채우는게 목표입니다.  
줄을 블록으로 꽉 채우면 그 줄이 사라지고 위에있던 블록들이 내려옵니다.
![설명2](https://user-images.githubusercontent.com/63161899/96385243-a1799600-11cd-11eb-91ec-3fd99601ec29.PNG)
![설명3](https://user-images.githubusercontent.com/63161899/96385244-a1799600-11cd-11eb-8384-4d1063f571a6.PNG)
![설명4](https://user-images.githubusercontent.com/63161899/96385245-a2122c80-11cd-11eb-9382-0fc3953f3433.PNG)

줄을 꽉 채우면 보스에게 데미지를 줄 수 있습니다.  
데미지는 한번에 많은 줄을 지울수록, 연속해서 줄을 지워 콤보를 쌓을수록 높아집니다.  
1줄 = 100  
2줄 = 200  
3줄 = 400  
4줄 = 600  
데미지 = 기본데미지 * (1 + 0.1*콤보) (단, 최대 콤보는 5)  
블록을 잘 쌓아 자쿰의 체력 5000을 깎아 무찌르세요.

---

알려진 문제점 및 패치노트 (2020. 10. 24. AM 01:20 update version 1.01 )  
1. ~~일부 T Spin에서 콤보가 비정상적으로 쌓임~~ -> 수정완료 (1.01)  
2. ~~항상 콤보 1 (배율 1.1배)에서 시작~~ -> 수정완료 (1.01)  
3. ~~버튼을 연속으로 누르거나, T-spin 등의 상황에서 여러번 줄을 지우는 버그~~ -> 수정완료 (1.01)  
4. 일부 기기에서 첫 블럭을 놓자마자 오류발생
