class Xh {
    constructor(x, y, bodyHeight, color) {
        this.x = x;
        this.y = y;
        this.bodyHeight = bodyHeight;
        this.color = color;
        this.tailMoveSpeed;
        if (random() > 0.5) { this.tailMoveSpeed = random(50, 60) } else { this.tailMoveSpeed = -random(50, 60); }
        this.tailMoveX = random(4, 5);
        this.eyeState = int(random(0, 3));
        this.mouthState = int(random(0, 5));
        this.capState = int(random(0, 7));
        this.cthState = int(random(0, 14));
        this.handsAngle = random(0, 0.2);
        this.acceleration = createVector(0, 0);
        this.velocity = createVector(0, 0);
        this.position = createVector(x, y);
        this.maxSpeed = 5;
        this.mass = 1;
    }
    applyForce(force) {
        let f = p5.Vector.div(force, this.mass);
        this.acceleration.add(f);
    }
    checkEdge() {
        if (this.position.x > width) {
            this.position.x = width;
            this.velocity.x = -this.velocity.x;
        } else if (this.position.x < 0) {
            this.position.x = 0;
            this.velocity.x = -this.velocity.x;
        }
        if (this.position.y > height) {
            this.position.y = height;
            this.velocity.y = -this.velocity.y;
        } else if (this.position.y < 0) {
            this.position.y = 0;
            this.velocity.y = -this.velocity.y;
        }
    }
    update() {
        this.checkEdge();
        this.velocity.add(this.acceleration);
        this.position.add(this.velocity);
        this.acceleration.mult(0);
        this.velocity.limit(this.maxSpeed);
    }
    followMouse() {
        this.applyForce(createVector(mouseX - this.position.x, mouseY - this.position.y).setMag(0.1));
    }
    display() {
        push();
        translate(this.position.x, this.position.y);
        rotate(this.velocity.heading() + PI / 2);
        fill(this.color);
        stroke(this.color);
        strokeWeight(1);
        //三角形
        let c_height = 30;
        let c_width = 20;
        beginShape()
        vertex(0, -c_height / 2);
        vertex(-c_width / 2, c_height / 2);
        vertex(c_width / 2, c_height / 2);
        endShape(CLOSE);
        pop();
    }
    f_display() {
        let x = this.position.x;
        let y = this.position.y;
        let bodyHeight = this.bodyHeight;
        let color = this.color;
        noStroke();
        //头饰
        switch (this.capState) {
            case 0: {
                fill(50);
                push();
                translate(x + gridSize * 1.6, y);
                scale(1, 1);
                beginShape();
                vertex(0, 2);
                vertex(-gridSize * 1.3, 2);
                vertex(-gridSize * 3, -gridSize * 2);
                vertex(-gridSize * 1.8, -gridSize * 1.3);
                vertex(-gridSize * 2, -gridSize * 3);
                vertex(-gridSize, -gridSize);
                vertex(0, 2);
                endShape();
                pop();
                push();
                translate(x + gridSize * 3.4, y);
                scale(-1, 1);
                beginShape();
                vertex(0, 2);
                vertex(-gridSize * 1.3, 2);
                vertex(-gridSize * 3, -gridSize * 2);
                vertex(-gridSize * 1.8, -gridSize * 1.3);
                vertex(-gridSize * 2, -gridSize * 3);
                vertex(-gridSize, -gridSize);
                vertex(0, 2);
                endShape();
                pop();
                break;
            }
            case 1: {
                fill(50);
                push();
                translate(x + gridSize * 1, y);
                beginShape();
                vertex(-gridSize * 0.5, 2);
                vertex(0, -gridSize * 1.5);
                vertex(gridSize * 0.5, 2);
                vertex(-gridSize * 0.5, 2);
                endShape();
                pop();
                push();
                translate(x + gridSize * 4, y);
                beginShape();
                vertex(-gridSize * 0.5, 2);
                vertex(0, -gridSize * 1.5);
                vertex(gridSize * 0.5, 2);
                vertex(-gridSize * 0.5, 2);
                endShape();
                pop();
                break;
            }
            case 2: {
                fill(250, 150, 0);
                push();
                translate(x + gridSize * 2.5, y);
                beginShape();
                vertex(-gridSize * 1.5, 2);
                vertex(gridSize * 1.5, 2);
                vertex(gridSize * 1.5, -gridSize);
                vertex(gridSize, -gridSize * 0.5);
                vertex(0, -gridSize * 1.2);
                vertex(-gridSize, -gridSize * 0.5);
                vertex(-gridSize * 1.5, -gridSize);
                vertex(-gridSize * 1.5, 2);
                endShape();
                fill(255);
                circle(-gridSize, -gridSize * 0.25, gridSize * 0.2);
                circle(0, -gridSize * 0.3, gridSize * 0.29);
                circle(gridSize, -gridSize * 0.25, gridSize * 0.2);
                pop();
                break;
            }
            case 3: {
                fill(50);
                push();
                translate(x + gridSize * 2.5, y);
                beginShape();
                vertex(-gridSize * 1.5, 2);
                vertex(gridSize * 1.5, 2);
                vertex(0, gridSize * -4.7);
                vertex(-gridSize * 1.5, 2);
                endShape();
                fill(255, 100);
                beginShape();
                vertex(-gridSize * 0.5, 2);
                vertex(-gridSize * 1.5, 2);
                vertex(0, gridSize * -4.7);
                vertex(-gridSize * 0.5, 2);
                endShape();
                pop();
                break;
            }
            case 4: {
                push();
                translate(x + gridSize * 2.5, y);
                let gradient = drawingContext.createLinearGradient(0, -gridSize * 4, 0, 0);
                gradient.addColorStop(0, "rgb(0,0,0)");
                gradient.addColorStop(0.5, "rgb(0,0,0)");
                gradient.addColorStop(1, "rgba(0,0,0,0)");
                drawingContext.fillStyle = gradient;
                beginShape();
                vertex(-gridSize * 1.5, 2);
                vertex(gridSize * 1.5, 2);
                vertex(gridSize * 0.5, -gridSize * 2);
                vertex(-gridSize * 0.5, -gridSize * 3);
                vertex(0, -gridSize * 4);
                vertex(-gridSize, -gridSize * 3);
                vertex(-gridSize * 0.5, -gridSize * 1.6);
                vertex(-gridSize * 1.5, 2);
                endShape();
                fill(0);
                circle(0, -gridSize * 4, gridSize);
                pop();
            }
        }
        //装饰
        switch (this.cthState) {
            case 1: {
                fill(100);
                push();
                translate(x + gridSize * 1.95, y + gridSize * 4.3);
                rotate(+sin(frameCount / 30) * 0.1);
                scale(-1, -1);
                beginShape();
                vertex(0, 0);
                vertex(gridSize, gridSize * 0.5);
                vertex(gridSize * 4, -gridSize);
                vertex(gridSize, gridSize);
                vertex(0, 0);
                endShape();
                push();
                translate(gridSize, gridSize * 0.5);
                rotate(-atan(0.5));
                for (let i = 1; i <= 3; i++) {
                    push();
                    translate(gridSize * i, -gridSize * 0.6);
                    scale(map(i, 1, 3, 1, 0.9));
                    fill(170);
                    beginShape();
                    vertex(0, gridSize * 0.5);
                    vertex(-gridSize * 0.3, 0);
                    vertex(0, -gridSize * 1);
                    vertex(gridSize * 0.3, 0);
                    vertex(0, gridSize * 0.5);
                    endShape();
                    pop();
                }
                pop();
                pop();
                fill(100);
                push();
                translate(x + gridSize * 3.05, y + gridSize * 4.3);
                rotate(-sin(frameCount / 30) * 0.1);
                scale(1, -1);
                beginShape();
                vertex(0, 0);
                vertex(gridSize, gridSize * 0.5);
                vertex(gridSize * 4, -gridSize);
                vertex(gridSize, gridSize);
                vertex(0, 0);
                endShape();
                push();
                translate(gridSize, gridSize * 0.5);
                rotate(-atan(0.5));
                for (let i = 1; i <= 3; i++) {
                    push();
                    translate(gridSize * i, -gridSize * 0.6);
                    scale(map(i, 1, 3, 1, 0.9));
                    fill(170);
                    beginShape();
                    vertex(0, gridSize * 0.5);
                    vertex(-gridSize * 0.3, 0);
                    vertex(0, -gridSize * 1);
                    vertex(gridSize * 0.3, 0);
                    vertex(0, gridSize * 0.5);
                    endShape();
                    pop();
                }
                pop();
                pop();
                break;
            }
            case 2: {
                fill(200);
                push();
                translate(x + gridSize * 1.95, y + gridSize * 4);
                rotate(+sin(frameCount / 30) * 0.1);
                scale(0.5);
                scale(-1, -1);
                beginShape();
                vertex(0, 0);
                vertex(gridSize, gridSize);
                vertex(gridSize * 8, 0);
                vertex(gridSize * 7, -gridSize * 1);
                vertex(gridSize * 6, 0);
                vertex(gridSize * 5, -gridSize * 1.5);
                vertex(gridSize * 4, 0);
                vertex(gridSize * 3, -gridSize * 2);
                vertex(gridSize * 2, 0);
                vertex(gridSize, -gridSize * 2.5);
                vertex(0, 0);
                endShape();
                pop();
                fill(200);
                push();
                translate(x + gridSize * 3.05, y + gridSize * 4);
                rotate(-sin(frameCount / 30) * 0.1);
                scale(0.5);
                scale(1, -1);
                beginShape();
                vertex(0, 0);
                vertex(gridSize, gridSize);
                vertex(gridSize * 8, 0);
                vertex(gridSize * 7, -gridSize * 1);
                vertex(gridSize * 6, 0);
                vertex(gridSize * 5, -gridSize * 1.5);
                vertex(gridSize * 4, 0);
                vertex(gridSize * 3, -gridSize * 2);
                vertex(gridSize * 2, 0);
                vertex(gridSize, -gridSize * 2.5);
                vertex(0, 0);
                endShape();
                pop();
                break;
            }
            case 3: {
                function drawBlock() {
                    fill(50, 100);
                    beginShape();
                    vertex(gridSize * 1.5, 0);
                    vertex(gridSize * 2, gridSize * 0.6);
                    vertex(gridSize * 4, 0);
                    vertex(gridSize * 2, -gridSize * 0.6);
                    vertex(gridSize * 1.5, 0);
                    endShape();
                    fill(255, 200);
                    beginShape();
                    vertex(gridSize * 1.5, 0);
                    vertex(gridSize * 2, gridSize * 0.6);
                    vertex(gridSize * 4, 0);
                    vertex(gridSize * 1.5, 0);
                    endShape();
                }
                push();
                translate(x + gridSize * 2.5, y + gridSize * 4.2);
                scale(1, 1);
                rotate(-PI / 8 - sin(frameCount / 30) * 0.1);
                drawBlock();
                rotate(PI / 8 - sin(frameCount / 30) * 0.1);
                drawBlock();
                rotate(PI / 8 - sin(frameCount / 30) * 0.1);
                drawBlock();
                pop();
                push();
                translate(x + gridSize * 2.5, y + gridSize * 4.2);
                scale(-1, 1);
                rotate(-PI / 8 - sin(frameCount / 30) * 0.1);
                drawBlock();
                rotate(PI / 8 - sin(frameCount / 30) * 0.1);
                drawBlock();
                rotate(PI / 8 - sin(frameCount / 30) * 0.1);
                drawBlock();
                pop();
                break;
            }
        }
        //脑袋
        {
            fill(color);
            rect(x, y, 5 * gridSize, 3 * gridSize, gridSize / 4);
        }
        //身体
        {
            let gradient = drawingContext.createLinearGradient(x + gridSize * 2.5, y + gridSize * 3, x + gridSize * 2.5, y + gridSize * this.bodyHeight + gridSize * 3);
            gradient.addColorStop(0, "rgb(0,0,0)");
            gradient.addColorStop(0.5, "rgb(0,0,0)");
            gradient.addColorStop(1, "rgba(0,0,0,0.5)");
            drawingContext.fillStyle = gradient;
            beginShape();
            vertex(x + gridSize * 2, y + gridSize * 3 - 1);
            vertex(x, y + gridSize * 3 + gridSize * bodyHeight);
            for (let ax = x - gridSize; ax < x + gridSize * 6; ax += 1) {
                vertex(ax, y + gridSize * 3 + gridSize * bodyHeight + gridSize / 5 + sin(ax / (gridSize / this.tailMoveX) - frameCount / this.tailMoveSpeed) * gridSize / 2);
            }
            vertex(x + gridSize * 5, y + gridSize * 3 + gridSize * bodyHeight);
            vertex(x + gridSize * 3, y + gridSize * 3 - 1);
            vertex(x + gridSize * 2, y + gridSize * 3 - 1);
            endShape();
            fill(color);
            beginShape();
            vertex(x + gridSize * 2, y + gridSize * 3);
            vertex(x, y + gridSize * 3 + gridSize * bodyHeight);
            for (let ax = x - gridSize; ax < x + gridSize * 6; ax += 1) {
                vertex(ax, y + gridSize * 3 + gridSize * bodyHeight + gridSize / 5 + sin(ax / (gridSize / this.tailMoveX) + frameCount / this.tailMoveSpeed) * gridSize / 2 + gridSize * 0.1);
            }
            vertex(x + gridSize * 5, y + gridSize * 3 + gridSize * bodyHeight);
            vertex(x + gridSize * 3, y + gridSize * 3);
            vertex(x + gridSize * 2, y + gridSize * 3);
            endShape();
        }
        //抠形
        {
            fill(255);
            beginShape();
            vertex(x + gridSize * 0.5, y + gridSize * 9);
            vertex(x - gridSize, y + gridSize * 9);
            vertex(x - gridSize, y + gridSize * 15);
            vertex(x + gridSize * 0.5, y + gridSize * 9);
            endShape();
            beginShape();
            vertex(x + gridSize * 4.5, y + gridSize * 9);
            vertex(x + gridSize * 6, y + gridSize * 9);
            vertex(x + gridSize * 6, y + gridSize * 15);
            vertex(x + gridSize * 4.5, y + gridSize * 9);
            endShape();
        }
        //胳膊
        {
            push();
            translate(x + gridSize * 2, y + gridSize * 4);
            rotate(this.handsAngle);
            fill(color);
            beginShape();
            vertex(0, 0);
            vertex(-gridSize * 3, 0);
            vertex(-gridSize * 3, gridSize * 0.2);
            vertex(0, gridSize * 1);
            endShape();
            circle(-gridSize * 3, gridSize * 0.1, gridSize * 0.2);
            pop();
            push();
            translate(x + gridSize * 3, y + gridSize * 4);
            rotate(-this.handsAngle);
            scale(-1, 1);
            fill(color);
            beginShape();
            vertex(0, 0);
            vertex(-gridSize * 3, 0);
            vertex(-gridSize * 3, gridSize * 0.2);
            vertex(0, gridSize * 1);
            endShape();
            circle(-gridSize * 3, gridSize * 0.1, gridSize * 0.2);
            pop();
        }
        //眼睛
        switch (this.eyeState) {
            case 0: {
                fill(255);
                circle(x + gridSize * 1, y + gridSize * 1.1, gridSize / 3);
                circle(x + gridSize * 4, y + gridSize * 1.1, gridSize / 3);
                break;
            }
            case 1: {
                fill(255);
                circle(x + gridSize * 1, y + gridSize * 1, gridSize / 5);
                circle(x + gridSize * 1, y + gridSize * 1.3, gridSize / 5);
                rectMode(CENTER);
                rect(x + gridSize * 1, y + gridSize * 1.15, gridSize / 5, gridSize * 0.3);
                rectMode(CORNER);
                circle(x + gridSize * 4, y + gridSize * 1, gridSize / 5);
                circle(x + gridSize * 4, y + gridSize * 1.3, gridSize / 5);
                rectMode(CENTER);
                rect(x + gridSize * 4, y + gridSize * 1.15, gridSize / 5, gridSize * 0.3);
                rectMode(CORNER);
                break;
            }
            case 2: {
                fill(255);
                arc(x + gridSize * 1, y + gridSize * 1.1, gridSize / 2, gridSize / 2, 0, -PI);
                arc(x + gridSize * 4, y + gridSize * 1.1, gridSize / 2, gridSize / 2, 0, -PI);
                break;
            }
        }
        //嘴巴
        switch (this.mouthState) {
            case 0: {
                push();
                translate(x + gridSize * 2.5, y + gridSize * 2);
                stroke(250);
                strokeWeight(0.5);
                noFill();
                beginShape();
                for (let ax = -PI * 3; ax < PI * 3; ax += 0.1) {
                    vertex(ax * gridSize / 20, cos(ax) * gridSize * 0.05);
                }
                endShape();
                noStroke();
                fill(this.color);
                pop();
                break;
            }
            case 1: {
                fill(100);
                rect(x + gridSize * 2, y + gridSize * 2, gridSize, gridSize * 0.5);
                fill(170);
                rect(x + gridSize * 2, y + gridSize * 2, gridSize, gridSize * 0.1);
                break;
            }
            case 2: {
                fill(160);
                beginShape();
                vertex(x + gridSize * 2, y + gridSize * 2);
                vertex(x + gridSize * 3, y + gridSize * 2);
                vertex(x + gridSize * 2.5, y + gridSize * 2.05);
                vertex(x + gridSize * 2, y + gridSize * 2);
                endShape();
                break;
            }
            case 3: {
                stroke(200);
                strokeWeight(0.8);
                noFill();
                arc(x + gridSize * 2.5, y + gridSize * 1.5, gridSize, gridSize, PI * 0.25, PI * 0.75);
                noStroke();
                fill(color);
                break;
            }
            case 4: {
                stroke(200);
                strokeWeight(0.8);
                noFill();
                arc(x + gridSize * 2.5, y + gridSize * 2.2, gridSize, gridSize, -PI * 0.75, -PI * 0.25);
                noStroke();
                fill(color);
                break;
            }
        }
    }
}
class XhCircle {
    constructor(pos, rate = 1) {
        this.position = pos;
        this.t = 44;
        this.isDead = false;
        this.rate = rate;
    }
    run() {
        this.t++;
        noFill();
        strokeWeight(0.5);
        stroke(0, 0, 0, map(this.t, 0, 130, 255, 0));
        circle(this.position.x, this.position.y, this.t*this.rate);
        if (this.t > 130) {
            this.isDead = true;
        }
        strokeWeight(1);
    }
}
class ControlCircle {
    constructor(player, pos, size = 200,command=0) {
        this.position = pos;
        this.size = size;
        this.pIn = false;
        this.nIn = false;
        this.player = player;
        this.command = command;
    }
    display() {
        noFill();
        stroke(0);
        if (this.nIn) {
            strokeWeight(2);
        }
        circle(this.position.x, this.position.y, this.size);
        strokeWeight(1);
        noStroke();
        fill(0);
        textSize(20);
        textAlign(CENTER, CENTER);
        text(this.command, this.position.x, this.position.y);
        noFill();
    }
    checkIn(pos) {
        return dist(this.position.x, this.position.y, pos.x, pos.y) < this.size / 2;
    }
    sendCommand() {
        axios
            .get(source+"api/setState/" + this.command)
            .then(function (response) {
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
    }
    run() {
        this.nIn = this.checkIn(this.player.position);
        if (this.nIn && !this.pIn) {
            this.sendCommand();
            xhCircleList.push(new XhCircle(this.position,4));
        }
        this.pIn = this.nIn;
        this.display();
    }
}