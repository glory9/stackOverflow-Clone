import pyodbc
from heapq import heapify, heappop

cnxn_str = (
    r'DRIVER=ODBC Driver 17 for SQL Server;'
    r'SERVER=(local)\SQLEXPRESS;'
    r'Trusted_Connection=yes;'
)
cnxn = pyodbc.connect(cnxn_str, autocommit=True)
cursor = cnxn.cursor()
cursor.execute("USE StackOverflow2010")
print("[SUCCESS] Connection To Database Successful..")


def get_top_questions(keywords):
    matching_id_counts = {}
    print("Searching For Matching Question Ids")

    for keyword in keywords:
        command = """
                SELECT Posts.Id
                FROM Posts
                WHERE Posts.PostTypeId = 1
                AND Posts.Title LIKE '%{}%'
                """.format(keyword)

        cursor.execute(command)
        matchingIds = [row[0] for row in cursor.fetchall()]

        for matchingId in matchingIds:
            matching_id_counts[matchingId] = matching_id_counts.get(matchingId, 0) + 1

    print("Computing Best Matches...")
    best_matches = get_best_matches(matching_id_counts)
    print(f"Top Matching Question Ids Are:")
    for match in best_matches:
        print(f"{match} matched {matching_id_counts[match]} times")

    print("\n\n Now Extracting Top Matching Questions...")
    top_questions = extract_questions_by_id(best_matches)

    print("[DONE] Closing database connection...")
    # cnxn.close()

    return top_questions


def get_best_matches(id_to_freq_map):
    freq_to_id_map = {}

    for eachId in id_to_freq_map:
        freq = id_to_freq_map[eachId]
        if freq in freq_to_id_map:
            freq_to_id_map[freq].append(eachId)

        else:
            freq_to_id_map[freq] = [eachId]

    # using a min heap as a max heap
    heap = [-1 * freq for freq in freq_to_id_map]
    heapify(heap)
    index = 0
    highest_occurrences = []
    while heap and index < 10:
        highest_occurrences.append(-1 * heappop(heap))

    best_matches = []
    full = False
    counter = 0

    for high_occurrence in highest_occurrences:
        for matching_id in freq_to_id_map[high_occurrence]:
            best_matches.append(matching_id)
            counter += 1

            if counter == 10:
                full = True
                break

        if full:
            break

    return best_matches


def extract_questions_by_id(matching_ids):
    top_questions = []

    for matching_id in matching_ids:
        sql_query = """
            SELECT Posts.Title, Posts.Score, Posts.AnswerCount, Users.DisplayName, Users.Reputation, Badges.Name
            FROM Posts
            JOIN Users
            ON Posts.OwnerUserId = Users.Id
            JOIN Badges
            ON Users.Id = Badges.UserId
            WHERE Posts.Id = {}
            """.format(matching_id)

        cursor.execute(sql_query)
        rows = cursor.fetchall()
        if not rows:
            continue
            
        user_badges = set()
        for row in rows:
            user_badges.add(row[5])

        question = [param for param in row]
        question[5] = [badge for badge in user_badges]

        top_questions.append(question)

    return top_questions

