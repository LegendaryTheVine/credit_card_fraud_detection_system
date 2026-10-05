# Instructor area (private)

Never share this folder with the student. Solutions live here.

- `lesson-plans/` - one file per day, mirrors `student/assignments/`
- `solutions/` - reference solutions, same layout as the student assignments
- `rubrics/` - grading criteria
- `review/` - PR review checklist and feedback template
- `slides-and-notes/` - theory material (Days 1-2) and talking points
- `progress-tracker.md` - status per day
- `scripts/` - publishing and safety scripts

## Publishing to the student
The student gets only `student/`.

1. Create a separate repo for the student (once) and clone it locally.
2. Run `scripts/publish_student.ps1 -Target <path-to-student-repo-clone>` to mirror `student/` into it.
3. Commit and push there. The student clones it and works on one branch per day.

The script runs `scripts/check_no_leaks.ps1` first and aborts if anything is wrong.

## Review loop
Student opens PR to their repo's `main` -> review with `review/pr-review-checklist.md` -> approve and merge -> update the tracker.
Recommended GitHub settings on the student repo: protect `main`, require a PR and your approval.
