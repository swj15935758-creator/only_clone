-- 부서별 평균 연봉인 4800 이상인 부서들 조회
SELECT
    DEPARTMENT_ID, -- 부서 ID
    -- 그룹핑 된 각 부서의 직원수를 EMPLOYEE_COUNT 별칭으로
    COUNT(*) AS EMPLOYEE_COUNT, -- 전체 행의 수 EMPLOYEE_COUNT 별칭으로
    -- 부서별 평균 연봉을 정수만 표시해서 AVG_SALARY 별칭으로
    ROUND(AVG(SALARY),0) AS AVG_SALARY
FROM
    EMPLOYEES
GROUP BY
    DEPARTMENT_ID -- 부서 ID가 같은 행들을 그룹핑
HAVING
    AVG(SALARY) >= %s -- 각 그룹에 조건을 부여, 평균 연봉이 보내준 평균 연봉 이상인
ORDER BY
    AVG_SALARY DESC -- 평균 연봉 내림차순 정렬