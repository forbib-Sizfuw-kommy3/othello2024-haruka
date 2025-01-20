class MinimaxAI(object):
    def face(self):
        return "🤔"

    def place(self, board, stone):
        best_x, best_y = -1, -1
        best_score = -float('inf')  # スコアの初期値を負の無限大にする

        for y in range(len(board)):
            for x in range(len(board[0])):
                if can_place_x_y(board, stone, x, y):
                    # 石を置いて、次の手を評価
                    score = self.minimax(board, stone, x, y, depth=3, maximizing_player=False)  # depthは探索の深さ

                    if score > best_score:
                        best_score = score
                        best_x, best_y = x, y

        if best_x != -1:
            return best_x, best_y
        else:
            return random_place(board, stone)

    def minimax(self, board, stone, x, y, depth, maximizing_player):
        # ミニマックス法の再帰関数

        # 石を置く
        new_board = [row[:] for row in board]  # ボードのコピーを作成
        # ... (石を置く処理を実装) ...

        # 探索の深さが0になったら評価値を返す
        if depth == 0:
            return self.evaluate_board(new_board, stone)  # 評価関数

        # 最大化プレイヤー(自分)の場合
        if maximizing_player:
            best_score = -float('inf')
            for next_y in range(len(new_board)):
                for next_x in range(len(new_board[0])):
                    if can_place_x_y(new_board, 3 - stone, next_x, next_y):  # 相手の番
                        score = self.minimax(new_board, 3 - stone, next_x, next_y, depth - 1, False)
                        best_score = max(score, best_score)
            return best_score

        # 最小化プレイヤー(相手)の場合
        else:
            best_score = float('inf')
            for next_y in range(len(new_board)):
                for next_x in range(len(new_board[0])):
                    if can_place_x_y(new_board, stone, next_x, next_y):  # 自分の番
                        score = self.minimax(new_board, stone, next_x, next_y, depth - 1, True)
                        best_score = min(score, best_score)
            return best_score
    def evaluate_board(self, board, stone):
      score = 0
      corners = [(0, 0), (0, len(board[0]) - 1), (len(board) - 1, 0), (len(board) - 1, len(board[0]) - 1)]

      for y in range(len(board)):
          for x in range(len(board[0])):
              if board[y][x] == stone:
                  if (x, y) in corners:
                      score += 10  # 隅は高得点
                  elif x == 0 or x == len(board[0]) - 1 or y == 0 or y == len(board) - 1:
                      score += 5   # 辺も得点
                  else:
                      score += 1
              elif board[y][x] == 3 - stone:
                  if (x, y) in corners:
                      score -= 10
                  elif x == 0 or x == len(board[0]) - 1 or y == 0 or y == len(board) - 1:
                      score -= 5
                  else:
                      score -= 1

      return score
class AdvancedAI(object):
    def face(self):
        return "🧠"  # より高度なAIを表す顔文字

    def place(self, board, stone):
        best_x, best_y = -1, -1
        best_score = -float('inf')  # スコアの初期値を負の無限大にする

        for y in range(len(board)):
            for x in range(len(board[0])):
                if can_place_x_y(board, stone, x, y):
                    # 石を置いて、次の手を評価
                    score = self.minimax(board, stone, x, y, depth=3, maximizing_player=False)  # depthは探索の深さ

                    if score > best_score:
                        best_score = score
                        best_x, best_y = x, y

        if best_x != -1:
            return best_x, best_y
        else:
            return random_place(board, stone)

    def evaluate_board(self, board, stone):
        score = 0

        # 1. 隅の石の数
        corners = [(0, 0), (0, len(board[0]) - 1), (len(board) - 1, 0), (len(board) - 1, len(board[0]) - 1)]
        for corner in corners:
            if board[corner[1]][corner[0]] == stone:
                score += 100  # 隅は非常に重要
            elif board[corner[1]][corner[0]] == 3 - stone:
                score -= 100

        # 2. 辺の石の数
        for y in range(len(board)):
            for x in range(len(board[0])):
                if (x == 0 or x == len(board[0]) - 1 or y == 0 or y == len(board) - 1) and (x, y) not in corners:  # 隅は除く
                    if board[y][x] == stone:
                        score += 20  # 辺も重要
                    elif board[y][x] == 3 - stone:
                        score -= 20

        # 3. 開放度 (石の周囲の空きマス数)
        for y in range(len(board)):
            for x in range(len(board[0])):
                if board[y][x] == stone:
                    liberty = 0
                    for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == 0:
                            liberty += 1
                    score -= liberty  # 開放度が高いほど減点

                elif board[y][x] == 3 - stone:
                    liberty = 0
                    for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == 0:
                            liberty += 1
                    score += liberty  # 相手の開放度が高いほど加点

        # 4. 確定石の数 (ひっくり返される可能性のない石)
        # ... (確定石の判定ロジックを実装) ...

        # 5. 潜在的な置ける場所の数
        my_potential_moves = 0
        opponent_potential_moves = 0
        for y in range(len(board)):
            for x in range(len(board[0])):
                if can_place_x_y(board, stone, x, y):
                    my_potential_moves += 1
                if can_place_x_y(board, 3 - stone, x, y):
                    opponent_potential_moves += 1
        score += my_potential_moves * 5  # 潜在的な置ける場所が多いほど加点
        score -= opponent_potential_moves * 5  # 相手の潜在的な置ける場所が多いほど減点

        return score
play_othello(AdvancedAI())
